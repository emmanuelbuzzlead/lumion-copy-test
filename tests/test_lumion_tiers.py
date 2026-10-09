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


def test_the_proof_fill_is_small():
    import tomllib
    cfg = tomllib.loads((ROOT / "clients" / "lumion" / "copy_test.toml").read_text(encoding="utf-8"))
    assert cfg["fill"]["target"] == 15
