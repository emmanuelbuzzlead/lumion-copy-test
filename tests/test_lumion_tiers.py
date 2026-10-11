"""The ProductEVO tier system as carried into the Lumion build.

Tier table thresholds, the scripts that build it, the one automatic refresh added, the exact last-send loader, and the
ProductEVO-only features that must stay off for Lumion. No database, no EmailBison, no model.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ROOT = Path(__file__).resolve().parent.parent

from app import angle_derivation, client, funnel, weekly_report  # noqa: E402


# --------------------------------------------------------------------------- the same system as ProductEVO

EVO = Path("C:/Claude_Code_GTM_Training/idpr-vertical-expander")


@pytest.mark.parametrize("name", ["funnel_dedupe.py", "history_backfill2.py", "sync_history_leads.py",
                                  "reply_backfill.py", "add_history_to_funnel.py", "tier_counts.py"])
def test_the_tier_scripts_are_ProductEVOs_verbatim(name):
    mine = (ROOT / name).read_text(encoding="utf-8").replace("\r\n", "\n")
    if not (EVO / name).exists():
        pytest.skip("ProductEVO checkout not on this machine")
    theirs = (EVO / name).read_text(encoding="utf-8").replace("\r\n", "\n")
    assert mine == theirs


def test_tier_thresholds_are_the_ones_ProductEVO_uses():
    sql = (ROOT / "history_backfill2.py").read_text(encoding="utf-8")
    assert re.search(r"> 120 THEN 2\s+WHEN \(CURRENT_DATE - lt\.last_date\) > 90 THEN 3\s+WHEN \(CURRENT_DATE - lt\.last_date\) > 60 THEN 4 ELSE 5", sql)
    assert "tier = 1, days_since_contact = NULL WHERE label = 'never_contacted'" in sql


def test_lumion_uses_ProductEVOs_sixty_day_floor_and_no_csv_gate():
    p = client.load("lumion")
    assert p.recontact_days == 60
    assert p.history_file is None and p.partition_hi is None
    from app import consultant_gate
    assert consultant_gate.active() is False       # the retired CSV gate must not run beside the tier table


def test_the_fill_engine_is_ProductEVOs_latest():
    src = (ROOT / "app" / "wave1_fill.py").read_text(encoding="utf-8")
    assert "fit_check_unjudged_reuse_companies" in src and "days_since_contact" in src
    assert "f.tier != 1" in src and "_targets_for" in src


# --------------------------------------------------------------------------- the one addition: automatic funnel refresh

def test_funnel_refresh_runs_both_scripts_in_order_and_throttles(monkeypatch):
    calls = []
    monkeypatch.setattr(funnel.runpy, "run_path", lambda path, run_name=None: calls.append(Path(path).name))
    monkeypatch.setattr(funnel, "_last", 0.0)
    out = funnel.refresh(force=True)
    assert calls == ["funnel_dedupe.py", "history_backfill2.py"] and set(out.values()) == {"ok"}
    assert funnel.refresh() == {"status": "recent"}          # the second call inside five minutes is skipped
    assert calls == ["funnel_dedupe.py", "history_backfill2.py"]


def test_funnel_refresh_stops_at_the_first_failure_and_says_which(monkeypatch):
    def boom(path, run_name=None):
        if Path(path).name == "funnel_dedupe.py":
            raise RuntimeError("db down")
    monkeypatch.setattr(funnel.runpy, "run_path", boom)
    out = funnel.refresh(force=True)
    assert out["funnel_dedupe.py"].startswith("failed: db down") and "history_backfill2.py" not in out


def test_sourcing_and_the_pool_refill_both_call_the_refresh():
    assert "funnel.refresh(run_id)" in (ROOT / "app" / "modes.py").read_text(encoding="utf-8")
    assert "funnel.refresh(run_id, force=True)" in (ROOT / "app" / "testgrid.py").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- ProductEVO-only features stay off

def test_self_learning_angles_are_off_for_lumion():
    assert angle_derivation.propose_new_test_angle("PDF") == {"status": "disabled_for_client"}
    assert angle_derivation.launch_new_test_angle("x", "PDF") == {"status": "disabled_for_client"}
    assert angle_derivation.check_derived_angles() == {"status": "disabled_for_client"}


def test_weekly_report_uses_lumions_offers_and_name():
    from app import testgrid
    cfg = testgrid.load_config()
    pitch = weekly_report._apply_client_pitch(cfg)
    assert set(pitch) == {"PDF", "AFTER5", "START"}
    assert pitch["AFTER5"].split(" \u2014")[0] == "After 5PM"
    assert weekly_report._client_name() == "Lumion"


def test_no_slack_text_names_ProductEVO():
    for f in ("app/wave1_fill.py", "app/weekly_report.py"):
        for n, line in enumerate((ROOT / f).read_text(encoding="utf-8").splitlines(), 1):
            if "ProductEVO" in line and 'slack' in line.lower() and line.strip().startswith(("slack.post", "f\":", '":')):
                pytest.fail(f"{f}:{n} {line.strip()[:80]}")


def test_unlabeled_saved_copy_is_never_guessed_for_lumion():
    from app import wave1_fill
    assert wave1_fill._guess_unlabeled() is False
    assert wave1_fill._name() == "Lumion"


# --------------------------------------------------------------------------- exact last send dates

import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("lumion_recent_contacts", ROOT / "lumion_recent_contacts.py")
lrc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lrc)


def _row(email, sent=None, status="sent", domain="acme.edu"):
    return {"sent_at": sent, "status": status,
            "lead": {"email": email, "custom_variables": [{"name": "domain", "value": domain}]}}


def test_each_lead_is_dated_by_the_newest_email_actually_sent(monkeypatch):
    pages = {1: {"meta": {"last_page": 1}, "data": [
        _row("a@acme.edu", "2026-06-01T10:00:00Z"), _row("a@acme.edu", "2026-06-05T10:00:00Z"),
        _row("a@acme.edu", None, "scheduled"),    # ignored below: pending means in flight, tested next
    ]}}
    monkeypatch.setattr(lrc.emailbison, "_get", lambda path, params=None: pages[(params or {}).get("page", 1)])
    rows, ok = lrc.read_campaign(9, date(2026, 5, 1))
    assert ok and rows == [("acme.edu", "a@acme.edu", 9, date.today())]      # a pending email makes it in flight, today


def test_a_finished_lead_keeps_its_real_last_send_date(monkeypatch):
    body = {"meta": {"last_page": 1}, "data": [_row("b@acme.edu", "2026-06-01T10:00:00Z"), _row("b@acme.edu", "2026-06-09T23:59:00Z")]}
    monkeypatch.setattr(lrc.emailbison, "_get", lambda path, params=None: body)
    rows, ok = lrc.read_campaign(9, date(2026, 5, 1))
    assert rows == [("acme.edu", "b@acme.edu", 9, date(2026, 6, 9))]


def test_a_lead_never_reached_falls_back_to_the_campaign_creation_day(monkeypatch):
    body = {"meta": {"last_page": 1}, "data": [{"sent_at": None, "status": "failed", "lead": {"email": "c@acme.edu", "custom_variables": []}}]}
    monkeypatch.setattr(lrc.emailbison, "_get", lambda path, params=None: body)
    rows, _ = lrc.read_campaign(9, date(2026, 5, 1))
    assert rows == [("acme.edu", "c@acme.edu", 9, date(2026, 5, 1))]


def test_free_mail_addresses_never_become_a_company(monkeypatch):
    body = {"meta": {"last_page": 1}, "data": [
        {"sent_at": "2026-06-01T10:00:00Z", "status": "sent", "lead": {"email": "d@gmail.com", "custom_variables": []}},
        {"sent_at": "2026-06-01T10:00:00Z", "status": "sent",
         "lead": {"email": "e@gmail.com", "custom_variables": [{"name": "website", "value": "https://www.shop.edu/"}]}}]}
    monkeypatch.setattr(lrc.emailbison, "_get", lambda path, params=None: body)
    rows, _ = lrc.read_campaign(9, None)
    assert [r[0] for r in rows] == ["shop.edu"]


def test_a_campaign_with_an_unread_page_is_reported_incomplete(monkeypatch):
    def get(path, params=None):
        p = (params or {}).get("page", 1)
        if p == 2:
            raise RuntimeError("boom")
        return {"meta": {"last_page": 2}, "data": [_row("f@acme.edu", "2026-06-01T10:00:00Z")]}
    monkeypatch.setattr(lrc.emailbison, "_get", get)
    monkeypatch.setattr(lrc.time, "sleep", lambda s: None)
    rows, ok = lrc.read_campaign(9, None)
    assert ok is False and len(rows) == 1


# --------------------------------------------------------------------------- proof-phase safety

def test_new_company_sourcing_is_off_until_asked_for(monkeypatch):
    from app import testgrid
    monkeypatch.delenv("POOL_REFILL_ENABLED", raising=False)
    assert testgrid.refill_pool("t") == {"status": "disabled"}


def test_the_fill_never_attaches_senders_when_the_flag_is_on():
    src = (ROOT / "app" / "wave1_fill.py").read_text(encoding="utf-8")
    assert "if settings.skip_sender_attach:" in src and src.index("if settings.skip_sender_attach:") < src.index("assign_senders(campaign_of, end, run_id)")


def test_the_fill_target_is_1000_per_angle():
    import tomllib
    cfg = tomllib.loads((ROOT / "clients" / "lumion" / "copy_test.toml").read_text(encoding="utf-8"))
    assert cfg["fill"]["target"] == 1000


# --------------------------------------------------------------------------- multi-page signal reading

from app.clients import jina  # noqa: E402

HOME = """# Acme Welding Academy
[Home](https://acmewelding.edu/) [Programs](https://acmewelding.edu/programs) [Admissions](https://acmewelding.edu/admissions)
[Contact Us](https://acmewelding.edu/contact-us) [Class Schedule](https://acmewelding.edu/class-schedule) [Blog](https://acmewelding.edu/blog/post-1)
[Facebook](https://facebook.com/acme) [Download Application](https://acmewelding.edu/files/application.pdf) ![logo](https://acmewelding.edu/logo.png)
[Email](mailto:info@acmewelding.edu) [Apply](/apply-now#top)
"""


def test_only_same_site_real_pages_are_candidates():
    urls = [u for _t, u in jina.extract_links(HOME, "acmewelding.edu")]
    assert "https://acmewelding.edu/admissions" in urls and "https://acmewelding.edu/apply-now" in urls
    assert not any("facebook" in u or "blog" in u or u.endswith(".png") or u.startswith("mailto") for u in urls)


def test_one_page_is_picked_per_signal_group():
    picked = jina.pick_pages(jina.extract_links(HOME, "acmewelding.edu"))
    assert picked[0].endswith(("/admissions", "/apply-now"))          # apply group
    assert "https://acmewelding.edu/contact-us" in picked              # hours group
    assert "https://acmewelding.edu/class-schedule" in picked          # dates group
    assert len(picked) == len(set(picked)) <= 3


def test_application_pdf_links_are_found_with_their_text():
    assert jina.pdf_links(HOME, "acmewelding.edu") == [("Download Application", "https://acmewelding.edu/files/application.pdf")]


def test_the_combined_text_marks_each_page_and_lists_the_pdfs(monkeypatch):
    pages = {"https://acmewelding.edu/admissions": "Apply: print the PDF and bring it in. " * 4,
             "https://acmewelding.edu/contact-us": "Office hours Monday to Friday 8am to 5pm. " * 4,
             "https://acmewelding.edu/class-schedule": "Next class starts January 12. " * 4}
    monkeypatch.setattr(jina, "_fetch_url", lambda u, n, links_summary=False: (HOME + "x" * 100) if u == "https://acmewelding.edu" else pages.get(u, ""))
    text = jina.website_text_with_pages("acmewelding.edu")
    assert "PAGE: https://acmewelding.edu/contact-us" in text and "Office hours Monday to Friday" in text
    assert "starts January 12" in text and "PDF LINKS FOUND ON THE SITE" in text and "application.pdf" in text


def test_a_dead_home_page_yields_nothing_and_never_raises(monkeypatch):
    monkeypatch.setattr(jina, "_fetch_url", lambda u, n, links_summary=False: "")
    assert jina.website_text_with_pages("dead.example") == ""


def test_the_copy_stage_reads_the_extra_pages():
    assert "jina.website_text_with_pages(domain)" in (ROOT / "app" / "stages" / "s5_copy.py").read_text(encoding="utf-8")


def test_hours_buried_deep_in_a_long_page_survive_the_trim():
    long = "intro line about the school. " * 400 + "\nOffice hours: Monday to Friday 8am to 5pm\n" + "more filler text here. " * 50
    out = jina._signal_trim(long, 1000, 600)
    assert "Office hours: Monday to Friday 8am to 5pm" in out and len(out) < 2200


# --------------------------------------------------------------------------- loading: refused leads are never counted as loaded

from app.clients import emailbison as eb  # noqa: E402
from app import scaling  # noqa: E402


def _fake_eb(monkeypatch, busy_ids):
    attached = []

    def send(method, path, payload=None, *a, **k):
        if path.endswith("/multiple"):
            return {"data": [{"id": 100 + i, "email": l["email"]} for i, l in enumerate(payload["leads"])]}
        if path.endswith("/attach-leads"):
            attached.extend(payload["lead_ids"])
            return {"data": {"success": True}}
        return {}

    def get(path, params=None):
        lid = int(path.rsplit("/", 1)[1])
        camps = [{"campaign_id": 999, "status": "in_sequence"}] if lid in busy_ids else [{"campaign_id": 5, "status": "stopped"}]
        return {"data": {"id": lid, "lead_campaign_data": camps}}

    monkeypatch.setattr(eb, "_send_retry", send)
    monkeypatch.setattr(eb, "_get", get)
    monkeypatch.setattr(eb, "ensure_custom_variables", lambda names: None)
    monkeypatch.setattr(eb, "_lead_for_upsert", lambda c: {"email": c["email"], "custom_variables": []})
    return attached


def test_a_lead_already_in_another_active_sequence_is_not_attached_and_is_reported(monkeypatch):
    attached = _fake_eb(monkeypatch, busy_ids={101})
    res = eb.push_leads(2030, [{"email": "a@x.edu"}, {"email": "b@x.edu"}, {"email": "c@x.edu"}], dry_run=False)
    assert attached == [100, 102]
    assert res["refused"] == {"b@x.edu": [999]} and res["attached"] == 2


def test_a_stopped_or_finished_lead_elsewhere_is_fine(monkeypatch):
    attached = _fake_eb(monkeypatch, busy_ids=set())
    res = eb.push_leads(2030, [{"email": "a@x.edu"}, {"email": "b@x.edu"}], dry_run=False)
    assert attached == [100, 101] and res["refused"] == {}


def test_load_leads_returns_only_the_leads_that_were_really_attached(monkeypatch):
    calls = {"updates": []}

    class Cur:
        def executemany(self, sql, rows):
            calls["updates"].append((sql.split()[1], list(rows)))

        def execute(self, sql, params=None):
            calls["updates"].append((sql.split()[1], [params]))

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(scaling.db, "cursor", lambda: Cur())
    monkeypatch.setattr(scaling.db, "log", lambda *a, **k: None)
    monkeypatch.setattr(scaling.emailbison, "push_leads",
                        lambda cid, rows, dry_run=False, on_upserted=None: {"refused": {"b@x.edu": [999]}})
    rows = [{"email": "a@x.edu"}, {"email": "b@x.edu"}]
    assert [r["email"] for r in scaling.load_leads(2030, rows, "run1")] == ["a@x.edu"]
    flagged = [r for kind, rr in calls["updates"] for r in rr if "another active" in str(r)]
    assert flagged, "the refused lead must be put back to needs_review with the reason"


def test_the_fill_pauses_when_the_shared_openrouter_balance_is_low(monkeypatch):
    from app import wave1_fill
    import httpx

    class R:
        def json(self):
            return {"data": {"total_credits": 1000.0, "total_usage": 990.0}}

    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    monkeypatch.delenv("OPENROUTER_MIN_BALANCE_USD", raising=False)
    monkeypatch.setattr(httpx, "get", lambda *a, **k: R())
    ok, left = wave1_fill._openrouter_ok()
    assert ok is False and round(left) == 10
    monkeypatch.setenv("OPENROUTER_MIN_BALANCE_USD", "5")
    assert wave1_fill._openrouter_ok()[0] is True


def test_a_failed_balance_lookup_never_blocks_the_fill(monkeypatch):
    from app import wave1_fill
    import httpx

    def boom(*a, **k):
        raise RuntimeError("network")

    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    monkeypatch.setattr(httpx, "get", boom)
    assert wave1_fill._openrouter_ok()[0] is True
    monkeypatch.setenv("OPENROUTER_MIN_BALANCE_USD", "0")
    assert wave1_fill._openrouter_ok() == (True, -1.0)
