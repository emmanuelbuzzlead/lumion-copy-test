"""Lumion build: the rules the spec and Emmanuel set (LUMION-SPEC.md, 2026-10-08).

Titles, exclusions, history gate, the per-client fit prompt, copy bans and the copy-test design.
Nothing here calls a vendor, a model or EmailBison.
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import client, company_fit, copy_rules, testgrid  # noqa: E402
from app.stages import s4_people  # noqa: E402

LUMION = client.CLIENTS_DIR / "lumion"
SPEC = LUMION / "spec" / "LUMION-SPEC.md"
TODAY = date(2026, 10, 8)

# Emmanuel's list, 2026-10-08, in order. The profile must carry exactly this.
EMMANUEL_TITLES = [
    "Owner", "Operator", "Founder", "School Director", "Campus Director", "Director of Admissions",
    "Admissions Director", "Director of Enrollment", "Enrollment Director", "Enrollment Manager",
    "Admissions Manager", "Enrollment Coordinator", "Admissions Coordinator", "Program Director",
    "Finance Director", "Director of Financial Aid", "Financial Aid Director", "Business Manager",
    "Operations Manager", "Director of Student Services", "Student Success Manager", "Marketing Director",
]


def _spec_exclude_titles() -> list[str]:
    text = SPEC.read_text(encoding="utf-8")
    block = text.split("### 3.2 Exclude", 1)[1].split("```text", 1)[1].split("```", 1)[0]
    return [t.strip() for t in block.replace("\n", " ").split(",") if t.strip()]


# --------------------------------------------------------------------------- profile

def test_profile_is_lumion_workspace_37_on_the_personal_host():
    p = client.load("lumion")
    assert (p.workspace_id, p.emailbison_base) == (37, "https://personal.buzzlead.io")
    assert p.emailbison_key_env == "LUMION_EMAIL_BISON_API_KEY"
    assert p.database == "lumion" and p.model_campaign_id == 1888
    assert p.default_mode == "copy-test" and p.declared_first is False
    assert (p.employee_min, p.employee_max) == (11, 200)


def test_titles_are_exactly_the_ones_emmanuel_gave_in_order():
    assert list(client.load("lumion").titles) == EMMANUEL_TITLES


def test_three_arms_declared_and_prompts_not_yet_handed_over():
    p = client.load("lumion")
    assert p.variant_names() == ("pdf-application", "after-5pm", "next-start-date")
    # The ONLY thing left is the three copies. Until they exist the profile must refuse to send.
    arms_with_prompts = [a for a in p.variant_names() if (p.prompts_dir / a / "prompt_email1.txt").exists()]
    if len(arms_with_prompts) < 3:
        assert not p.is_complete_for_sending


def test_copy_windows_are_the_spec_intersection():
    p = client.load("lumion")
    assert (p.email1_min_chars, p.email1_max_chars) == (380, 460)
    assert (p.email2_min_chars, p.email2_max_chars) == (600, 699)


# --------------------------------------------------------------------------- titles

@pytest.mark.parametrize("title", EMMANUEL_TITLES)
def test_every_declared_title_is_selectable(title):
    assert s4_people.score_title(title, 40) > 0, title


def test_declared_titles_rank_in_the_order_given():
    f = lambda t: s4_people.score_title(t, 40)
    assert f("Owner") > f("Operator") > f("Founder") > f("School Director") > f("Director of Admissions")
    assert f("Director of Admissions") > f("Marketing Director")


@pytest.mark.parametrize("title", [
    "Owner / Lead Instructor", "Owner & Lead Instructor", "Master Barber / Owner",
    "Owner and Instructor", "Founder, Lead Welding Instructor",
])
def test_include_wins_over_an_excluded_word(title):
    assert s4_people.persona_banned(title)             # the exclusion word is really there
    assert s4_people.score_title(title, 25) > 0, title


@pytest.mark.parametrize("title", [
    "Welding Instructor", "CDL Instructor", "Cosmetology Instructor", "Admissions Representative",
    "Admissions Advisor", "Enrollment Advisor", "Enrollment Counselor", "Career Services Coordinator",
    "Externship Coordinator", "Student Services Coordinator", "Financial Aid Officer",
    "Executive Assistant", "Receptionist", "Registrar", "Provost", "Dean of Students", "Professor",
    "Teacher", "Certified Flight Instructor", "Licensed Massage Therapist", "Truck Driver",
    "Assistant to the Owner", "Executive Assistant to the Director of Admissions",
])
def test_excluded_people_are_never_selected(title):
    assert s4_people.score_title(title, 40) == 0, title


def test_every_spec_exclude_title_scores_zero_unless_it_contains_a_declared_title():
    declared = [set(re.findall(r"[a-z&]+", t.lower())) for t in EMMANUEL_TITLES]
    leaked = []
    for title in _spec_exclude_titles():
        words = set(re.findall(r"[a-z&]+", title.lower()))
        contains_declared = any(d <= words for d in declared)
        # Emmanuel's list deliberately includes "Admissions Coordinator", which the spec excluded.
        if not contains_declared and s4_people.score_title(title, 40) != 0:
            leaked.append(title)
    assert not leaked, leaked


def test_keywords_match_whole_words_only():
    # "rep" must not match "Reporting", "unit" must not match "Community" (spec 3.3).
    assert not s4_people.persona_banned("Director of Community Reporting")
    assert not s4_people.persona_banned("Campus Director")
    assert s4_people.persona_banned("Customer Service Rep")


def test_the_coordinator_exception_is_only_for_declared_titles():
    assert s4_people.score_title("Enrollment Coordinator", 30) > 0
    assert s4_people.score_title("Admissions Coordinator", 30) > 0
    assert s4_people.score_title("Marketing Coordinator", 30) == 0
    assert s4_people.score_title("Assistant Enrollment Coordinator", 30) == 0   # assistant stays banned


def test_office_manager_is_not_a_target():
    assert s4_people.score_title("Office Manager", 15) == 0


# --------------------------------------------------------------------------- fit prompt

def test_lumion_judges_schools_not_product_makers():
    system = company_fit._system()
    assert "Lumion" in system and "trade schools" in system
    assert "ProductEVO" not in system and "manufactur" not in system.lower().replace("contract manufacturer", "")
    for v in client.load("lumion").verticals:
        assert v in system
    assert '"fit"' in system                      # the JSON reply contract survived .format()


# --------------------------------------------------------------------------- copy rules

def _violations(text, arm="after-5pm"):
    copy_rules.set_context(arm, "Pat")
    return copy_rules.check(text, "", rules=copy_rules.load("lumion"))


GOOD = ("Your Google listing says the office at Acme Welding closes at 5.\n\n"
        "Lumion answers those calls in your school's voice and books a real callback.\n\n"
        "Want me to send over what the first 30 days looked like for Arclabs Welding?")


def test_a_clean_email_passes_the_client_rules():
    assert _violations(GOOD) == []


@pytest.mark.parametrize("bad", [
    GOOD.replace("closes at 5", "closes at 5 - every day"),
    GOOD + " Plans start at $99 a month.",
    GOOD.replace("books a real callback", "books 40% more callbacks"),
    GOOD.replace("books a real callback", "stops you losing students"),
    GOOD.replace("Lumion answers", "Unlike HubSpot, Lumion answers"),
    GOOD.replace("Lumion answers", "Our platform answers"),
    "Most schools miss calls after 5.\n\n" + GOOD.split("\n\n", 1)[1],
    GOOD.replace("first 30 days looked like for Arclabs Welding?", "first 30 days looked like for Arclabs Welding."),
    "Hi there: " + GOOD,
])
def test_client_bans_catch_what_the_spec_forbids(bad):
    assert _violations(bad), bad


def test_every_arm_must_carry_the_first_30_days_question():
    for arm in ("pdf-application", "after-5pm", "next-start-date"):
        assert _violations("Short note with no question at all?", arm), arm


# --------------------------------------------------------------------------- copy test design

def test_copy_test_has_three_angles_each_with_a_prompt_folder_that_is_a_declared_arm():
    cfg = tomllib.loads((LUMION / "copy_test.toml").read_text(encoding="utf-8"))
    arms = set(client.load("lumion").variant_names())
    assert len(cfg["angles"]) == 3
    assert set(cfg["angle_prompts"]) == set(cfg["angles"])
    assert set(cfg["angle_prompts"].values()) == arms


def test_every_declared_vertical_belongs_to_exactly_one_segment():
    cfg = tomllib.loads((LUMION / "copy_test.toml").read_text(encoding="utf-8"))
    seen: dict[str, str] = {}
    for seg, verticals in cfg["segments"].items():
        for v in verticals:
            assert v not in seen, f"{v} in {seen[v]} and {seg}"
            seen[v] = seg
    assert set(seen) - {"Tier 2 - previously emailed"} == set(client.load("lumion").verticals)
    assert set(cfg["segment_caps"]) == set(cfg["segments"])


def test_the_engine_deals_every_segment_evenly_across_the_three_angles():
    cfg = tomllib.loads((LUMION / "copy_test.toml").read_text(encoding="utf-8"))
    contacts = [{"email": f"p{i}@s{i % 7}.edu", "vertical": v}
                for i, v in enumerate(client.load("lumion").verticals * 90)]
    dealt = testgrid.deal(contacts, cfg)
    assert set(dealt) == set(cfg["angles"])
    per_seg = {}
    for angle, rows in dealt.items():
        for r in rows:
            per_seg.setdefault(r["segment"], {}).setdefault(angle, 0)
            per_seg[r["segment"]][angle] += 1
    for seg, counts in per_seg.items():
        assert max(counts.values()) - min(counts.values()) <= 1, (seg, counts)


def test_school_map_covers_every_vertical_and_names_only_allowed_schools():
    m = json.loads((LUMION / "school-map.json").read_text(encoding="utf-8"))
    allowed = {"approved", "closest", "unapproved"}
    assert all(v["status"] in allowed for v in m["verticals"].values())
    for vertical in client.load("lumion").verticals:
        assert vertical in m["_engine_vertical_to_map_key"], vertical
    assert "{similar_school}" in m["cta_template"] and "first 30 days" in m["fallback_cta"]


def test_proof_schools_are_never_prospects():
    dnc = (LUMION / "do_not_contact.txt").read_text(encoding="utf-8").lower()
    m = json.loads((LUMION / "school-map.json").read_text(encoding="utf-8"))
    for v in m["verticals"].values():
        if v["status"] == "approved":
            assert v["school"].lower() in dnc, v["school"]
