"""ProductEVO copy test: 3 angle campaigns, each holding every segment, read per segment.

Design (Troy, 2026-09-26): one campaign per angle, each carrying 1,000 contacts from every
segment, each contact tagged with its vertical. The angle is read across the whole
campaign (3x the volume of a 9-cell grid) and the segment is read afterwards from the tag.

Three jobs, all read-only against EmailBison and additive to the database:

  deal()       split contacts across the angle campaigns at random, balanced per segment,
               so the three audiences are the same by construction
  read_grid()  per (angle, segment) counts straight from outcome_events -- exact per lead,
               no apportioning of campaign totals
  decide()     the pre-declared rules in clients/productevo/copy_test.toml; names a
               champion only when the rules are met, otherwise says why not yet

champion_campaign() is what s7_push consults so later batches join the winner instead of
opening a new campaign. Nothing here sends; the approval gate is untouched.
"""

from __future__ import annotations

import hashlib
import math
import tomllib
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import db

CLIENTS_DIR = Path(__file__).resolve().parent.parent / "clients"
# Kept for callers that name ProductEVO's file on purpose.
CONFIG_PATH = CLIENTS_DIR / "productevo" / "copy_test.toml"

_TABLES = """
CREATE TABLE IF NOT EXISTS copy_test_campaigns (
    angle       TEXT NOT NULL,
    campaign_id BIGINT NOT NULL,
    launched_at TIMESTAMPTZ,
    is_primary  BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (angle, campaign_id)
);
ALTER TABLE copy_test_campaigns ADD COLUMN IF NOT EXISTS is_primary BOOLEAN NOT NULL DEFAULT TRUE;
CREATE TABLE IF NOT EXISTS copy_test_champion (
    id          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    angle       TEXT NOT NULL,
    campaign_id BIGINT NOT NULL,
    separated   BOOLEAN NOT NULL,
    reason      TEXT,
    decided_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def load_config(path: Path | None = None) -> dict | None:
    """The ACTIVE client's copy_test.toml, or None. It used to be ProductEVO's file for every
    client, so IDPR's nightly review could have run ProductEVO's test and auto-expansion
    (found 2026-09-27)."""
    if path is None:
        from .client import current_name
        path = CLIENTS_DIR / current_name() / "copy_test.toml"
    if not path.exists():
        return None
    with path.open("rb") as fh:
        return tomllib.load(fh)


def ensure_tables() -> None:
    with db.cursor() as cur:
        cur.execute(_TABLES)
        # Migration, 2026-10-01: the table used to allow exactly one campaign per angle.
        # Troy now clones a stalled campaign under a new name (e.g. "Stopped Leads
        # PEVO_W1_MMM") to keep delivering, and the clone needs to count toward the SAME
        # angle's score. Drop the old angle-only primary key if it is still there.
        cur.execute("""SELECT conname, array_length(conkey, 1) AS ncols FROM pg_constraint
                       WHERE conrelid = 'copy_test_campaigns'::regclass AND contype = 'p'""")
        row = cur.fetchone()
        if row and row["ncols"] == 1:
            cur.execute(f'ALTER TABLE copy_test_campaigns DROP CONSTRAINT "{row["conname"]}"')
            cur.execute("""ALTER TABLE copy_test_campaigns
                           ADD PRIMARY KEY (angle, campaign_id)""")


def _register_for_reply_sweep(angle: str, campaign_id: int) -> None:
    """Make stop_on_reply.sweep_all() see this campaign too.

    Found 2026-10-01: ve_campaigns (the table that sweep reads) was completely empty.
    Every Wave 1 copy-test campaign was registered in copy_test_campaigns for SCORING,
    but never here, so real replies sitting in EmailBison were never pulled into
    contacts.replied_at / outcome_events -- the day-7 decision would have read zero
    signal from campaigns that actually had dozens of replies. copy_test_campaigns and
    ve_campaigns are two separate registries; a campaign now needs both.
    """
    from . import db as _db
    with _db.cursor() as cur:
        cur.execute(
            """INSERT INTO ve_campaigns (campaign_id, campaign_name, vertical, batch_id,
                                         run_id, pushed_lead_count)
               VALUES (%s,%s,%s,%s,%s,0)
               ON CONFLICT (campaign_id) DO NOTHING""",
            (campaign_id, f"copy-test-{angle}-{campaign_id}", _db.POOL_VERTICAL,
             f"copy-test-{angle}", f"copy-test-{angle}"))


def register_campaign(angle: str, campaign_id: int, launched_at: datetime | None = None) -> None:
    """Registers the PRIMARY campaign for an angle -- the one wave1_fill loads fresh
    leads into and auto_expand_champion scales. See sync_duplicate_campaigns() for
    Troy's renamed clones, which count toward scoring but are never the load target."""
    ensure_tables()
    with db.cursor() as cur:
        cur.execute(
            """INSERT INTO copy_test_campaigns (angle, campaign_id, launched_at, is_primary)
               VALUES (%s,%s,%s,TRUE)
               ON CONFLICT (angle, campaign_id) DO UPDATE
                  SET is_primary = TRUE,
                      launched_at = COALESCE(EXCLUDED.launched_at, copy_test_campaigns.launched_at)""",
            (angle, campaign_id, launched_at))
    _register_for_reply_sweep(angle, campaign_id)


def sync_duplicate_campaigns(run_id: str | None = None) -> dict:
    """Find EmailBison campaigns Troy cloned off a registered one by name, and fold them
    into that angle's score.

    Troy, 2026-10-01: "I kept the naming similar with just suffixes" -- when a campaign
    stalls (EmailBison marks it finished with most leads never contacted, usually a
    sender-capacity wall) he clones it under a new name, e.g. base "PEVO_W1_MMM" ->
    "Stopped Leads PEVO_W1_MMM", to keep delivering to the same audience. The clone's
    replies are really that angle's replies and must count, but it is never itself the
    load target or the champion -- only the ORIGINAL registered row (is_primary) is.
    Matches case-insensitively on the primary campaign's own base name appearing
    anywhere in a candidate's name, so a prefix or suffix either side is fine.
    """
    from .clients import emailbison
    ensure_tables()
    with db.cursor() as cur:
        cur.execute("SELECT angle, campaign_id FROM copy_test_campaigns WHERE is_primary")
        primaries = {r["angle"]: int(r["campaign_id"]) for r in cur.fetchall()}
    if not primaries:
        return {"found": {}}
    all_campaigns = emailbison.list_campaigns()
    by_id = {int(c["id"]): c for c in all_campaigns}
    found: dict[str, list[int]] = {}
    with db.cursor() as cur:
        for angle, primary_id in primaries.items():
            base_name = (by_id.get(primary_id) or {}).get("name") or ""
            if not base_name.strip():
                continue
            base_lower = base_name.strip().lower()
            matches = [c for c in all_campaigns
                      if int(c["id"]) != primary_id
                      and base_lower in (c.get("name") or "").strip().lower()]
            new_ids = []
            for c in matches:
                cur.execute(
                    """INSERT INTO copy_test_campaigns (angle, campaign_id, is_primary)
                       VALUES (%s,%s,FALSE)
                       ON CONFLICT (angle, campaign_id) DO NOTHING""",
                    (angle, int(c["id"])))
                if cur.rowcount:
                    new_ids.append(int(c["id"]))
                    _register_for_reply_sweep(angle, int(c["id"]))
            if new_ids:
                found[angle] = new_ids
    if found:
        db.log(run_id, "testgrid", f"sync_duplicate_campaigns: newly folded in {found}")
    return {"found": found}


def segment_of(vertical: str | None, cfg: dict) -> str | None:
    for seg, verticals in cfg["segments"].items():
        if vertical in verticals:
            return seg
    return None


def deal(contacts: list[dict], cfg: dict) -> dict[str, list[dict]]:
    """Deal contacts to angles at random, exactly balanced within each segment.

    Ordering is by a seeded hash of the email, not list position, so no angle gets the
    top of a ranked list; then cards go round the angles in turn, so the counts differ by
    at most one. Contacts outside every segment are left out, never guessed into one.
    """
    angles = list(cfg["angles"])
    seed = cfg["rules"]["random_deal_seed"]
    out: dict[str, list[dict]] = {a: [] for a in angles}
    by_seg: dict[str, list[dict]] = {}
    for c in contacts:
        seg = segment_of(c.get("vertical"), cfg)
        if seg:
            by_seg.setdefault(seg, []).append(c)
    default_cap = int(cfg["rules"]["per_segment_per_campaign"])
    caps = cfg.get("segment_caps") or {}
    for seg, rows in by_seg.items():
        cap = int(caps.get(seg, default_cap))
        rows.sort(key=lambda c: hashlib.sha256(f"{seed}:{c['email'].strip().lower()}".encode()).hexdigest())
        rows = rows[: cap * len(angles)]
        for i, c in enumerate(rows):
            out[angles[i % len(angles)]].append({**c, "segment": seg})
    return out


def wilson(successes: int, total: int, z: float = 1.959964) -> tuple[float, float]:
    if total <= 0:
        return 0.0, 0.0
    p = successes / total
    d = 1 + z * z / total
    centre = p + z * z / (2 * total)
    spread = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total)
    return max(0.0, (centre - spread) / d), min(1.0, (centre + spread) / d)


def read_grid() -> list[dict]:
    """One row per (angle, vertical): leads, replied, interested, booked, positive.

    Sums across every campaign registered under an angle, primary AND any name-matched
    duplicate (sync_duplicate_campaigns) -- a clone Troy made to keep delivering to a
    stalled campaign's audience is still that angle's traffic for scoring purposes.
    """
    ensure_tables()
    with db.cursor() as cur:
        cur.execute(
            """SELECT tc.angle, ct.vertical,
                      count(DISTINCT ct.email) AS leads,
                      count(DISTINCT ct.email) FILTER (WHERE oe.event_type='replied')    AS replied,
                      count(DISTINCT ct.email) FILTER (WHERE oe.event_type='interested') AS interested,
                      count(DISTINCT ct.email) FILTER (WHERE oe.event_type='booked')     AS booked,
                      count(DISTINCT ct.email) FILTER (WHERE oe.event_type IN ('interested','booked')) AS positive
                 FROM copy_test_campaigns tc
                 JOIN contacts ct ON ct.eb_campaign_id = tc.campaign_id
                 LEFT JOIN outcome_events oe
                        ON oe.email = ct.email AND oe.campaign_id = tc.campaign_id
                WHERE ct.vertical IS NOT NULL
                GROUP BY tc.angle, ct.vertical""")
        return [dict(r) for r in cur.fetchall()]


def rollup(grid: list[dict], cfg: dict) -> dict:
    """{'by_angle': {...}, 'by_segment': {seg: {angle: {...}}}} from read_grid() rows."""
    zero = {"leads": 0, "replied": 0, "interested": 0, "booked": 0, "positive": 0}
    by_angle = {a: dict(zero) for a in cfg["angles"]}
    by_seg: dict[str, dict[str, dict]] = {}
    for r in grid:
        seg = segment_of(r["vertical"], cfg)
        if seg is None or r["angle"] not in by_angle:
            continue
        cell = by_seg.setdefault(seg, {a: dict(zero) for a in cfg["angles"]})[r["angle"]]
        for k in zero:
            by_angle[r["angle"]][k] += int(r[k] or 0)
            cell[k] += int(r[k] or 0)
    return {"by_angle": by_angle, "by_segment": by_seg}


def _value(row: dict, booked_weight: int) -> int:
    return int(row["interested"]) + booked_weight * int(row["booked"])


def decide(by_angle: dict[str, dict], launched_at: datetime, cfg: dict,
           now: datetime | None = None) -> dict:
    """Apply the pre-declared rules. Returns status: frozen | extend | decided | no_data."""
    r = cfg["rules"]
    now = now or datetime.now(timezone.utc)
    if launched_at.tzinfo is None:
        launched_at = launched_at.replace(tzinfo=timezone.utc)
    freeze_end = launched_at + timedelta(days=int(r["freeze_days"]))
    positives = sum(int(a["positive"]) for a in by_angle.values())
    base = {"positives": positives, "freeze_ends": freeze_end}
    if now < freeze_end:
        return {**base, "status": "frozen",
                "reason": f"inside the {r['freeze_days']}-day freeze (ends {freeze_end:%d %b}); nothing is judged or edited"}
    if positives < int(r["min_positive_total"]):
        return {**base, "status": "extend",
                "reason": f"{positives} positive replies, need {r['min_positive_total']}; "
                          f"extend {r['extend_days_if_short']} days rather than guess"}
    w = int(r["booked_weight"])
    ranked = sorted(by_angle.items(),
                    key=lambda kv: _value(kv[1], w) / max(int(kv[1]["leads"]), 1), reverse=True)
    (top, t), (second, s) = ranked[0], ranked[1]
    t_rate = _value(t, w) / max(int(t["leads"]), 1)
    s_rate = _value(s, w) / max(int(s["leads"]), 1)
    if t_rate <= s_rate:
        return {**base, "status": "extend", "reason": f"{top} and {second} are level; no winner yet"}
    t_low, _ = wilson(_value(t, w), int(t["leads"]))
    _, s_high = wilson(_value(s, w), int(s["leads"]))
    separated = t_low > s_high
    return {**base, "status": "decided", "winner": top, "runner_up": second,
            "separated": separated,
            "reason": f"{top} leads {second} ({t_rate:.2%} vs {s_rate:.2%} per lead); "
                      + ("intervals clear, a firm win" if separated
                         else "intervals still overlap, a lean not a proof; challenger keeps running")}


def record_champion(angle: str, campaign_id: int, separated: bool, reason: str) -> None:
    ensure_tables()
    with db.cursor() as cur:
        cur.execute(
            """INSERT INTO copy_test_champion (id, angle, campaign_id, separated, reason)
               VALUES (1,%s,%s,%s,%s)
               ON CONFLICT (id) DO UPDATE
                  SET angle=EXCLUDED.angle, campaign_id=EXCLUDED.campaign_id,
                      separated=EXCLUDED.separated, reason=EXCLUDED.reason, decided_at=now()""",
            (angle, campaign_id, separated, reason))


def champion_campaign() -> int | None:
    """The campaign new batches should join, or None while the test is still open."""
    if load_config() is None:
        return None
    try:
        ensure_tables()
        with db.cursor() as cur:
            cur.execute("SELECT campaign_id FROM copy_test_champion WHERE id = 1")
            row = cur.fetchone()
        return int(row["campaign_id"]) if row else None
    except Exception:
        return None


def unused_verticals(cfg: dict, n: int) -> list[str]:
    """Declared verticals not already feeding any Wave 1 segment, most-recently-declared last."""
    from . import client
    used = {v for verts in cfg["segments"].values() for v in verts}
    try:
        declared = list(client.profile().verticals)
    except Exception:
        return []
    return [v for v in declared if v not in used][:n]


def auto_expand_champion(winner: str, run_id: str | None, n: int | None = None) -> dict:
    """Once an angle has won decisively, PROPOSE scaling it -- do not spend on it.

    Troy, 2026-09-28: every spend needs a cost estimate and his explicit go-ahead first,
    "nothing may auto-resume paid work behind his back." A winning message used to trigger
    real sourcing and copy spend (champion_topup + new verticals) with no estimate and no
    wait. Now it only posts the plan and an estimate to Slack and records a pending
    proposal; run_approved_expansion() below does the real work, and only after
    approve_expansion() has been called (from a one-off script, once Troy replies).
    """
    from . import client
    from .clients import slack
    cfg = load_config()
    sc = cfg.get("scaling") or {}
    n = n or int(sc.get("expand_verticals", 3))
    ensure_tables()
    with db.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS copy_test_expansions (
            id SERIAL PRIMARY KEY, angle TEXT NOT NULL, vertical TEXT NOT NULL,
            queued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            approved BOOLEAN NOT NULL DEFAULT FALSE, executed_at TIMESTAMPTZ)""")
        cur.execute("ALTER TABLE copy_test_expansions ADD COLUMN IF NOT EXISTS approved BOOLEAN NOT NULL DEFAULT FALSE")
        cur.execute("ALTER TABLE copy_test_expansions ADD COLUMN IF NOT EXISTS executed_at TIMESTAMPTZ")
        cur.execute("SELECT 1 FROM copy_test_expansions LIMIT 1")
        if cur.fetchone():
            return {"expanded": [], "reason": "already proposed or scaled once for this test"}
        cur.execute("SELECT campaign_id FROM copy_test_campaigns WHERE angle=%s AND is_primary", (winner,))
        row = cur.fetchone()
    if not row:
        return {"expanded": [], "reason": f"no campaign registered for {winner}"}
    champion = int(row["campaign_id"])
    variant = (cfg.get("angle_prompts") or {}).get(winner)
    if not variant:
        return {"expanded": [], "reason": f"no prompt folder for {winner} in [angle_prompts]"}
    new_verticals = unused_verticals(cfg, n)
    with db.cursor() as cur:
        cur.executemany("INSERT INTO copy_test_expansions (angle, vertical) VALUES (%s,%s)",
                        [(winner, v) for v in new_verticals] or [(winner, "(none left)")])
    topup = int(sc.get("champion_topup", 1000))
    per_vertical = int(sc.get("leads_per_new_vertical", 300))
    est_leads = topup + per_vertical * len(new_verticals)
    est_cost = round(est_leads * 0.02 + len(new_verticals) * 3, 2)   # ~2c/lead copy, ~$3/vertical to source
    slack.post(f":seedling: *Copy test winner: {winner}* (campaign {champion}). Proposed scale-up, NOT started:\n"
               f"- top up {topup} more never-contacted leads from the tested segments\n"
               f"- try {len(new_verticals)} new vertical(s): {', '.join(new_verticals) or 'none left'}, "
               f"{per_vertical} leads each\n"
               f"- about {est_leads:,} leads total, estimated ${est_cost}\n"
               f"Reply *go* to run this, or tell me to change the numbers first.")
    return {"expanded": new_verticals, "status": "proposed", "estimated_leads": est_leads,
            "estimated_cost": est_cost, "champion": champion, "variant": variant}


def approve_expansion() -> dict:
    """Call this once Troy replies 'go' to the Slack proposal above. Marks it approved;
    the next 2-hourly resume() tick then actually runs run_approved_expansion()."""
    ensure_tables()
    with db.cursor() as cur:
        cur.execute("""UPDATE copy_test_expansions SET approved = TRUE
                       WHERE executed_at IS NULL RETURNING angle""")
        rows = cur.fetchall()
    return {"approved_for": [r["angle"] for r in rows]}


def run_approved_expansion(run_id: str | None = None) -> dict:
    """The real spend, only after approve_expansion() has been called. Safe to call every
    tick: a no-op unless there is an approved, not-yet-executed proposal."""
    from . import client, modes, scaling
    from .clients import slack
    ensure_tables()
    with db.cursor() as cur:
        cur.execute("""SELECT DISTINCT angle FROM copy_test_expansions
                       WHERE approved AND executed_at IS NULL""")
        winners = [r["angle"] for r in cur.fetchall()]
    if not winners:
        return {"status": "nothing_approved"}
    winner = winners[0]
    cfg = load_config()
    sc = cfg.get("scaling") or {}
    with db.cursor() as cur:
        cur.execute("SELECT vertical FROM copy_test_expansions WHERE angle=%s AND approved AND executed_at IS NULL",
                    (winner,))
        new_verticals = [r["vertical"] for r in cur.fetchall() if r["vertical"] != "(none left)"]
        cur.execute("SELECT campaign_id FROM copy_test_campaigns WHERE angle=%s AND is_primary", (winner,))
        champion = int(cur.fetchone()["campaign_id"])
    variant = (cfg.get("angle_prompts") or {}).get(winner)
    run_id = run_id or "scale-winner-" + __import__("time").strftime("%Y%m%dT%H%M%S")
    db.start_run(run_id)

    tested = [v for verts in cfg["segments"].values() for v in verts]
    results = [("tested segments", scaling.feed_campaign(
        champion, variant, tested, int(sc.get("champion_topup", 1000)), run_id))]
    profile = client.profile()
    for v in new_verticals:
        try:
            modes.run_source(profile, v, 3000, companies_only=True)
            results.append((v, scaling.feed_campaign(
                champion, variant, [v], int(sc.get("leads_per_new_vertical", 300)), run_id)))
        except Exception as exc:
            db.log(run_id, "testgrid", f"scaling into {v} failed: {exc}", level="warn")
            results.append((v, {"loaded": 0, "error": str(exc)[:120]}))
    lines = [f"*{winner} scaled* (campaign {champion}):"]
    for label, r in results:
        lines.append(f"- {label}: {r.get('loaded', 0)} new leads loaded"
                     + (f" ({r['error']})" if r.get("error") else ""))
    slack.post("\n".join(lines))
    with db.cursor() as cur:
        cur.execute("UPDATE copy_test_expansions SET executed_at = now() WHERE angle=%s AND approved AND executed_at IS NULL",
                    (winner,))
    db.finish_run(run_id, "complete", "; ".join(f"{l}={r.get('loaded', 0)}" for l, r in results))
    return {"expanded": new_verticals, "results": results}


def evaluate_and_record() -> dict:
    """Daily entry point: read the grid, apply the rules, record a champion if decided."""
    cfg = load_config()
    if cfg is None:
        return {"status": "no_config"}
    ensure_tables()
    try:
        sync_duplicate_campaigns()
    except Exception as exc:
        db.log(None, "testgrid", f"sync_duplicate_campaigns failed: {exc}", level="warn")
    with db.cursor() as cur:
        cur.execute("SELECT angle, campaign_id, launched_at FROM copy_test_campaigns WHERE is_primary")
        camps = {r["angle"]: r for r in cur.fetchall()}
    if len(camps) < len(cfg["angles"]) or any(c["launched_at"] is None for c in camps.values()):
        return {"status": "no_data", "reason": "test campaigns are not all registered and launched"}
    launched = min(c["launched_at"] for c in camps.values())
    roll = rollup(read_grid(), cfg)
    verdict = decide(roll["by_angle"], launched, cfg)
    if verdict["status"] == "decided":
        record_champion(verdict["winner"], int(camps[verdict["winner"]]["campaign_id"]),
                        verdict["separated"], verdict["reason"])
        if verdict["separated"]:
            verdict["auto_expand"] = auto_expand_champion(verdict["winner"], None)
    return {**verdict, **roll}
