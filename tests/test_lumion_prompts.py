"""The nine Lumion prompts (three angles x research, email 1, email 2).

No model is called. These prove the files load through the engine's own loader, carry the spec's guardrails verbatim, and that
the spec's reference drafts and the prompts' own examples sit inside the length windows and pass every client rule.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import client, copy_rules, prompts, validator  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("gen_lumion_prompts", ROOT / "scripts" / "gen_lumion_prompts.py")
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

ARMS = ("pdf-application", "after-5pm", "next-start-date")
FILES = ("prompt_research.txt", "prompt_email1.txt", "prompt_email2.txt")


def _violations(text: str, arm: str, report: str = "") -> list[str]:
    copy_rules.set_context(arm, "Pat")
    return copy_rules.check(text, report, rules=copy_rules.load("lumion"))


# --------------------------------------------------------------------------- loading

def test_profile_is_complete_for_sending_with_all_nine_files():
    p = client.load("lumion")
    assert not p.fell_back and p.is_complete_for_sending
    for arm in ARMS:
        for f in FILES:
            assert (p.prompts_dir / arm / f).exists(), (arm, f)
            assert "LEGACY" not in p.prompt_source(f, arm)


@pytest.mark.parametrize("arm", ARMS)
def test_every_prompt_loads_and_renders_with_the_engines_slots(arm):
    r = prompts.load("prompt_research.txt", arm)
    out = r.render_user(company_profile_data="Name: Acme", person_profile_data="Name: Pat", website_text="Welding school in Tulsa.",
                        serper_news_results="", serper_competitor_results="", today="October 08, 2026", cutoff="October 2025")
    assert "October 08, 2026" in out and "Welding school" in out
    e1 = prompts.load("prompt_email1.txt", arm)
    assert "RESEARCH" in e1.render_user(company_name="Acme", job_title="Owner", research_report="R", client_overview="x")
    e2 = prompts.load("prompt_email2.txt", arm)
    assert "EMAIL 1 SENT" in e2.render_user(company_name="Acme", job_title="Owner", research_report="R", email_1_output="E1", client_overview="x")
    assert r.temperature <= 0.4 and e1.temperature >= 0.6


@pytest.mark.parametrize("arm", ARMS)
def test_the_arms_are_distinct(arm):
    others = [a for a in ARMS if a != arm]
    mine = prompts.load("prompt_email1.txt", arm).system
    for o in others:
        assert mine != prompts.load("prompt_email1.txt", o).system


# --------------------------------------------------------------------------- guardrails

@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("f", ("prompt_email1.txt", "prompt_email2.txt"))
def test_email_prompts_embed_the_spec_blocks_verbatim(arm, f):
    system = prompts.load(f, arm).system
    for block in (gen.GUARDRAIL, gen.CLIENT_BANS, gen.APPROVED_SCHOOLS):
        assert block in system
    assert "between 380 and 460" in system and "between 550 and 699" in system
    assert "Drew Jones" in system and "first 30 days" in system
    assert "{SIMILAR_TYPE}" in system        # the engine never fills this, the model does from the research


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("f", ("prompt_email1.txt", "prompt_email2.txt"))
def test_email_prompt_size_is_close_to_the_spec_range(arm, f):
    n = len(prompts.load(f, arm).system.split())
    assert 600 <= n <= 1400, n        # spec asks 600 to 1,200; a little over is accepted for the verbatim guardrail block


@pytest.mark.parametrize("arm", ARMS)
def test_research_prompt_carries_the_school_map_gates_and_this_arms_signal(arm):
    system = prompts.load("prompt_research.txt", arm).system
    assert "SIMILAR SCHOOL TYPE MAP" in system and "healthcare school" in system and "NONE" in system
    assert "ICP GATES" in system and "Hard no fires first" in system
    assert "none_found" in system and "OPENER_FACT" in system and "SIMILAR_TYPE:" in system
    signal = {"pdf-application": "SIGNAL_APPLICATION_FORMAT", "after-5pm": "SIGNAL_OFFICE_CLOSE_TIME",
              "next-start-date": "SIGNAL_NEXT_START_DATE"}[arm]
    assert signal in system
    for other in set(("SIGNAL_APPLICATION_FORMAT", "SIGNAL_OFFICE_CLOSE_TIME", "SIGNAL_NEXT_START_DATE")) - {signal}:
        assert other not in system, f"{arm} research must not ask for {other}"


def test_every_email_prompt_has_a_signal_free_path():
    for arm in ARMS:
        assert "PATH B" in prompts.load("prompt_email1.txt", arm).system
        e2 = prompts.load("prompt_email2.txt", arm).system
        assert "never introduce the signal" in e2


def test_a_research_report_in_the_expected_format_is_usable():
    report = ("SCHOOL: Lone Star Welding Academy, Tulsa OK\nVERTICAL: welding\nPROGRAMS: Pipe welding, structural welding\n"
              "ICP_GATE: PASS private owner operated multi month programs\nicp_fit: HIGH\nSIMILAR_TYPE: welding school\n"
              "SIGNAL_OFFICE_CLOSE_TIME: 17:00\nSIGNAL_WEEKEND_HOURS: closed\nSIGNAL_SOURCE: website\n"
              "OPENER_FACT: The site says the office closes at 5 on weekdays.\n"
              "SUMMARY: A private welding school with day and evening programs. It serves adults changing careers.")
    assert validator.research_is_usable(report)


# --------------------------------------------------------------------------- the copy itself

DRAFTS = {
    "pdf-application": (
        "Noticed the enrollment application on Lone Star Dental's site is a PDF students print and bring in.\n\n"
        "Someone applying to a dental assisting program is usually filling it out on their phone at 10pm. Lumion turns your application into a mobile form that saves their progress and texts them to finish, so more inquiries become enrolled students.\n\n"
        "Want me to send over what the first 30 days looked like for a similar healthcare school?",
        "One more thought on the application piece.\n\n"
        "When the only way to apply is a PDF, the students who quit halfway never show up anywhere. They don't call or email. They enroll at a school that let them finish on their phone.\n\n"
        "Lumion swaps that PDF for a mobile application that saves progress, texts a reminder to anyone who stops partway, and drops every finished application into your admissions queue. Payment plans sit inside the same flow, so a student can pick one before they close the tab.\n\n"
        "A similar healthcare school uses Lumion for enrollment. Want me to send over what their first 30 days looked like?"),
    "after-5pm": (
        "Your Google listing says the office at Lone Star Welding closes at 5.\n\n"
        "People looking at a welding program usually work a full shift and call on the way back from the job site. Lumion answers those calls in your school's voice, books a real callback, and texts the application while they're still on the line, so the call turns into a start date.\n\n"
        "Want me to send over what the first 30 days looked like for a similar welding school?",
        "One more thought on the after hours calls.\n\n"
        "Someone who calls a welding school at 7pm and hits voicemail rarely leaves a message. They call the next school on the list, and whoever picks up books the tour.\n\n"
        "Lumion's phone agent answers every call in your school's voice, books a real callback, and texts the caller your application before they hang up. It remembers earlier texts, forms and calls from the same person, so nobody repeats themselves. Your team starts the morning with booked callbacks instead of missed calls.\n\n"
        "A similar welding school works with Lumion. Want me to send over what their first 30 days looked like?"),
    "next-start-date": (
        "Saw the next HVAC class at Lone Star Trade starts January 12.\n\n"
        "Schools usually have a pile of inquiries from the last 90 days that nobody reached twice. Lumion texts every one of them and puts payment plans right in the enrollment flow, so students say yes on the spot and fill the seats you still have.\n\n"
        "Want me to send over what the first 30 days looked like for a similar trade school?",
        "One more thought on the January class.\n\n"
        "The quickest seats to fill belong to people who already asked about the program. Plenty of them went quiet after one call or one email because nobody followed up a second time. A short text is an easy way back into the conversation.\n\n"
        "Lumion texts every inquiry from the last 90 days about the January 12 start and keeps following up until they apply or say no. When tuition is the holdup, payment plans sit right inside the enrollment flow so they can say yes on the spot.\n\n"
        "A similar trade school runs on Lumion. Want me to send over what their first 30 days looked like?"),
}


@pytest.mark.parametrize("arm", ARMS)
def test_the_spec_reference_drafts_sit_in_the_windows_and_pass_every_rule(arm):
    e1, e2 = DRAFTS[arm]
    assert 380 <= len(e1) <= 460, len(e1)
    assert 550 <= len(e2) <= 699, len(e2)
    assert validator.validate_email1(e1).ok, validator.validate_email1(e1).violations
    assert validator.validate_email2(e2).ok, validator.validate_email2(e2).violations
    assert _violations(e1, arm) == [] and _violations(e2, arm) == []


def _examples(text: str) -> list[str]:
    blocks = re.split(r"\n\n(?=GOOD EXAMPLE)", text.strip())
    return [b.split("\n", 1)[1].strip() for b in blocks if b.startswith("GOOD EXAMPLE")]


@pytest.mark.parametrize("arm", ARMS)
def test_every_good_example_inside_the_prompts_obeys_its_own_rules(arm):
    e1s, e2s = _examples(gen.ANGLES[arm]["e1_good"]), _examples(gen.ANGLES[arm]["e2_good"])
    assert len(e1s) == 2 and len(e2s) == 1
    for t in e1s:
        assert 380 <= len(t) <= 460, (arm, len(t), t[:40])
        assert _violations(t, arm) == [], (arm, _violations(t, arm))
        assert validator.validate_email1(t).ok, (arm, validator.validate_email1(t).violations)
    for t in e2s:
        assert 550 <= len(t) <= 699, (arm, len(t))
        assert _violations(t, arm) == []
        assert validator.validate_email2(t).ok, (arm, validator.validate_email2(t).violations)


@pytest.mark.parametrize("arm", ARMS)
def test_the_fallback_cta_closes_a_signal_free_email_cleanly(arm):
    body = ("People weighing a welding program usually decide late at night, on their phone, with the application half done.\n\n"
            "Lumion turns an application into a mobile form that saves their progress and texts them to finish, so more inquiries become enrolled students.\n\n"
            "Want me to send over what the first 30 days looked like for a school doing your volume?")
    assert _violations(body, arm) == []


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("f", ("prompt_research.txt", "prompt_email1.txt", "prompt_email2.txt"))
def test_no_prompt_names_a_customer_school(arm, f):
    system = prompts.load(f, arm).system
    for name in ("Hoosier Trade", "Arclabs", "Savant Aesthetics", "Berry Best", "Tripleten", "Iron Circle", "Train For The Crane"):
        assert name not in system, (arm, f, name)
