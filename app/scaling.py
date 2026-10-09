"""Feed a campaign from never-contacted companies, end to end.

pick companies -> find and verify people -> write copy in the campaign's angle -> load into
EmailBison -> report. Used for two things (Troy, 2026-09-27):
  - sourcing only "a considerable amount" for the copy test, not the whole never-contacted
    pool (source_contacts with a company budget)
  - scaling a winning angle: keep feeding the champion from never-contacted companies in the
    tested segments, then from newly expanded verticals (feed_campaign)
Companies are taken makers-first (website confirmed a real product brand), dead-website
companies last, never a company that has replied, never one already worked.
"""
from __future__ import annotations

import json
import math

from . import db
from .clients import emailbison


def pick_companies(verticals: list[str], n: int) -> list[dict]:
    if n <= 0:
        return []
    with db.cursor() as cur:
        cur.execute(
            """SELECT DISTINCT ON (s.domain) s.domain, s.vertical, s.payload
               FROM staged_companies s JOIN company_funnel f ON f.domain = s.domain
               WHERE s.verdict = 'KEEP' AND s.vertical = ANY(%s)
                 AND s.found_at IS NULL AND s.consumed_at IS NULL
                 AND f.tier = 1 AND NOT coalesce(f.replied, false)
               ORDER BY s.domain""", (verticals,))
        rows = cur.fetchall()
    rank = {"MAKER": 0, None: 1, "UNKNOWN": 1, "NO_SITE": 2}
    rows.sort(key=lambda r: (rank.get((r["payload"] or {}).get("_site_fit"), 1),
                             hash(r["domain"]) % 100000))
    out = []
    for r in rows[:n]:
        c = r["payload"] if isinstance(r["payload"], dict) else json.loads(r["payload"] or "{}")
        c.update(domain=r["domain"], vertical=r["vertical"], _tier="vertical")
        out.append(c)
    return out


def source_contacts(companies: list[dict], run_id: str) -> list[dict]:
    """Find and verify people at these companies; bank them as 'verified'."""
    from .stages import s4_people
    if not companies:
        return []
    people, _stats = s4_people.build(companies, run_id)
    try:
        db.reserve_contacts(people, run_id, None, status="verified")
    except Exception as exc:
        db.log(run_id, "scaling", f"contacts not persisted: {exc}", level="warn")
    by_v: dict[str, list[str]] = {}
    for c in companies:
        by_v.setdefault(c["vertical"], []).append(c["domain"])
    for v, doms in by_v.items():
        db.mark_found(v, doms)
    return people


def load_leads(campaign_id: int, rows: list[dict], run_id: str) -> list[dict]:
    """Chunks of 50; a rejected chunk is retried one lead at a time.

    Found 2026-10-01: this never passed on_upserted, so none of the leads it loaded ever
    got their EmailBison lead id written back to contacts.eb_lead_id. That id is what
    stop_on_reply needs to pull a sibling off a reply and to check the Meeting Booked
    tag, so every lead this function has ever loaded was invisible to both.
    """
    loaded: list[dict] = []
    for i in range(0, len(rows), 50):
        chunk = rows[i:i + 50]
        try:
            emailbison.push_leads(campaign_id, chunk, dry_run=False, on_upserted=db.record_lead_ids)
            loaded += chunk
            continue
        except Exception:
            pass
        for r in chunk:
            try:
                emailbison.push_leads(campaign_id, [r], dry_run=False, on_upserted=db.record_lead_ids)
                loaded.append(r)
            except Exception as exc:
                with db.cursor() as cur:
                    cur.execute("UPDATE contacts SET status='needs_review', drop_reason=%s WHERE email=%s",
                                (f"EmailBison refused: {str(exc)[:150]}", r["email"]))
    if loaded:
        with db.cursor() as cur:
            cur.executemany("""UPDATE contacts SET status='pushed', eb_campaign_id=%s, run_id=%s,
                               updated_at=now() WHERE email=%s""",
                            [(campaign_id, run_id, r["email"]) for r in loaded])
    return loaded


def feed_campaign(campaign_id: int, variant: str, verticals: list[str], target_leads: int,
                  run_id: str, yield_per_company: float = 0.5, max_rounds: int = 4) -> dict:
    """Load up to target_leads NEW leads into campaign_id, sourcing only what that needs."""
    from .stages import s5_copy
    loaded = sourced = companies_used = 0
    for _ in range(max_rounds):
        need = target_leads - loaded
        if need <= 0:
            break
        with db.cursor() as cur:
            cur.execute("""SELECT email, first_name, last_name, title, company_domain, company_name, vertical
                           FROM contacts c LEFT JOIN company_funnel f ON f.domain = c.company_domain
                           WHERE c.status='verified' AND c.eb_campaign_id IS NULL
                             AND coalesce(c.first_name,'') <> '' AND c.vertical = ANY(%s)
                             AND NOT coalesce(f.replied, false)
                           LIMIT %s""", (verticals, int(need * 1.4) + 5))
            banked = [dict(r) for r in cur.fetchall()]
        if len(banked) < need:
            companies = pick_companies(verticals, math.ceil((need - len(banked)) / yield_per_company * 1.2))
            if not companies and not banked:
                break
            companies_used += len(companies)
            fresh = source_contacts(companies, run_id)
            sourced += len(fresh)
            banked += [dict(p, company_name=p.get("company_name")) for p in fresh]
        for c in banked:
            c["copy_variant"] = variant
        ready, _ = s5_copy.run(banked[: int(need * 1.4) + 5], run_id)
        got = load_leads(campaign_id, ready[:need], run_id)
        spare = [r["email"] for r in ready[need:]]
        if spare:
            with db.cursor() as cur:
                cur.execute("UPDATE contacts SET status='verified' WHERE email = ANY(%s) AND status='draft'", (spare,))
        loaded += len(got)
        if not got and not banked:
            break
    return {"campaign_id": campaign_id, "loaded": loaded, "people_sourced": sourced,
            "companies_worked": companies_used}
