# Lumion Outbound Spec for Claude Code

**Prepared:** October 8, 2026 · **Prepared with:** Claude (BuzzLead GTM, built to the gtm-project-architect addendum structure and pipeline contract)
**Client slug:** `lumion` · **EmailBison workspace:** `Lumion` (assumed, see VERIFY-8) · **Sender persona:** Drew Jones, Lumion (andrew.jones@lumion.ai)
**Meeting goal:** 50 qualified meetings per month · **Status:** Draft for engineer review

## 0. Read this first

This is one spec that contains everything Claude Code needs for the Lumion outbound build: the ICP, the title include and exclude lists, the vertical to similar-school map, three new copy angles with reference drafts, and the build and run instructions. Read it top to bottom.

Rules for the run:

1. Do not invent facts. Anything marked **VERIFY** is unconfirmed. Build around it, do not assert it in copy beyond what the reference drafts already say, and list it back to the engineer at the first review gate.
2. Case study numbers never appear in copy. School names only. Lumion's 2025 Impact Report and competitive matrix were promised in the March 2026 onboarding form and never arrived.
3. No dash characters in any email text. Casual founder voice. Positive framing, never "stop losing".
4. Gate first: hard-no criteria fire before any yes. Default to No on ambiguity. Smaller clean lists beat large dirty ones.
5. No Clay. All list building, enrichment and scoring run in Claude Code and the GTM pipeline.

## 1. Client context

- **Company:** Lumion, lumion.ai. AI-powered enrollment platform built for private trade schools and career colleges. US-wide. *(Onboarding Form, Research Overview)*
- **Products:** Engagement suite (lead capture, SMS and communications, CRM, dynamic enrollment forms; value in 1 to 2 weeks), Payments (in-house tuition payment plans, the moat product), Voice AI (24/7 phone agent in the school's own voice, books real callbacks, texts links mid-call, remembers the caller's earlier texts, forms and calls; added June 2026). *(Onboarding Form, engagement-evolution.md section 7)*
- **Core problem solved:** Four leaks between click and first class: lead capture, follow-up speed (especially SMS), application to enrollment drop-off, and students who cannot pay upfront. *(Onboarding Form)*
- **Why it works as outbound:** The real opponent is inertia. Only 21 of 876 lost deals (2.4%) named a competitor (the deck lists TFC 5 and Salesforce 2). Ghosting is the top loss reason (26% overall, 40% in the latest period). The loans objection fell from 62% to under 2% of losses after the Payments repositioning. *(Win/Loss deck)*
- **Approved case studies, names only:** Hoosier Trade School, Arclabs Welding, Savant Aesthetics Institute, CDL Training of Tampa, Dasmesh Truck Driving School, Berry Best Phlebotomy, Tripleten, Coding Temple, Iron Circle, Sanders Flight Training Center, Train For The Crane, RiseAero, FlexAir. *(engagement-evolution.md section 8)*
- **Buyer language:** "Light blue collar." They want results (more seats, faster enrollment, faster tuition), not features, and will not follow complex selling points. Plain words, money and seats, no SaaS vocabulary. *(Onboarding Form)*
- **Hard constraints:** No pricing in email, pricing questions deflected to a call. If the contact is the wrong person, ask for the right one. Email 1 is written CTA first so it survives truncation. *(engagement-evolution.md section 9)*
- **Length rules:** The account runs E1 at 380 to 460 characters and E2 under 700. The pipeline requires E1 300 to 500 and E2 600 to 800. Use the intersection: **E1 380 to 460, E2 600 to 699.**

## 2. ICP

**One sentence:** Private, for-profit, owner-operated US trade schools with one location or a small chain, 11 to 200 employees and $600K to $1.2M or more in revenue, running multi-month hands-on programs of $3K or more tuition, with manual admissions and no way for students to pay in installments. *(Onboarding Form, engagement-evolution.md section 4)*

| Gate | Pass | Fail (hard no) |
| --- | --- | --- |
| Ownership | Private, for-profit, owner-operated | Public, nonprofit, university, community college, K-12 or CTE district program |
| Size | 11 to 200 employees | Under 11 or over 200 |
| Revenue | $600K to $1.2M sweet spot, up to about $5M | Over about $5M, or clearly under $500K (except new-school plays) |
| Program | Hands-on, multi-month, tuition $3K or more | Under $3K, short courses, continuing ed, adult basic ed, GED or ESL |
| Funding | Not heavily dependent on Title IV | Mostly Title IV funded |
| Fit | Physical training component (online coding and cyber bootcamps are the one approved exception) | Online-only outside bootcamps, employer-paid enrollment |

**Sourcing rule:** Pull from regulatory directories (state boards of education and licensing boards, NACCAS, ACCSC, ABHES, FMCSA TPR registry), not NAICS or business-database pulls. NAICS returns too many community colleges and universities. All trade schools must register with their state board and those registries are public. Pilot states: TX, FL, CA, OH, GA. *(Onboarding Form, GTM Brief, engagement-evolution.md section 4)*

**Vertical priority by win rate** (1,512 deals, March 2026). *(Win/Loss deck)*

| Tier | Vertical | Win rate | Note |
| --- | --- | --- | --- |
| A | Coding / Tech | 68.1% | $6,525 ACV, 41 day cycle |
| A | Cyber Security | 65.2% | IronCircle partnership working |
| A | Dental Assisting | 45.9% | 90 deals, 20 day close |
| B | Welding / NDT | 47.2% | 9 day median close |
| B | HVAC / Plumbing | 47.4% | Zero churn |
| B | Massage Therapy | 42.9% | Needs a stronger value story |
| C | CDL / Trucking | 36.2% | Lead with Payments |
| C | Cosmetology | 30.5% | Most volume, 33% of losses are ghosting |
| C | Flight / Aviation | 17.8% | Shelved for active spend |

**Caveat to keep visible:** The win-rate ranking may be biased toward Lumion's referral network and is not ACV weighted. Nobody has corrected for it since April. (VERIFY-9)

**Ruled out as verticals:** Pet grooming, adult basic education, continuing education, restaurant management, lifeguard and recreational scuba, wind turbine technician, real estate pre-licensing, standalone phlebotomy, EKG and pharmacy tech. Commercial diving folds into Welding/NDT as a keyword. *(engagement-evolution.md section 5)*

## 3. Titles

### 3.1 Include (proposed)

The onboarding form says the owner/operator is almost always the final decision-maker, and at larger schools enrollment, admissions and finance also buy. This list is derived from that and was not run through the title-skill intake, so the engineer confirms it.

**11 to 50 employees:**
```text
Owner, Co-Owner, Owner/Operator, Founder, Co-Founder, President, CEO, Chief Executive Officer, Managing Director, Executive Director, School Director, Campus Director, Operator
```

**51 to 200 employees (inherits the list above):**
```text
Owner, Co-Owner, Owner/Operator, Founder, Co-Founder, President, CEO, Chief Executive Officer, Managing Director, Executive Director, School Director, Campus Director, Operator, Director of Admissions, Director of Enrollment, Head of Admissions, Head of Enrollment, VP of Enrollment, Director of Marketing, Head of Marketing, VP of Marketing, COO, Chief Operating Officer, CFO, Director of Finance
```

### 3.2 Exclude

One list. Full titles first, then standalone keywords.

```text
Executive Assistant, Administrative Assistant, Receptionist, Customer Service Representative, Customer Success Manager, Account Manager, Technical Support Specialist, Help Desk Analyst, Help Desk Manager, Bookkeeper, Accountant, Staff Accountant, Legal Assistant, Paralegal, Software Engineer, Data Analyst, Data Engineer, HR Specialist, Warehouse Manager, Quality Control Manager, Lab Technician, Maintenance Technician, Field Technician, Logistics Coordinator, Inventory Manager, Payroll Specialist, Recruiting Coordinator, Property Manager, Franchisor, Social Media Manager, Email Marketing Manager, Web Designer, Graphic Designer, SEO Specialist, PPC Specialist, Sales Development Representative, Business Development Representative, Inside Sales Representative, Account Executive, Branch Manager, Regional Manager, District Manager, Area Manager, Site Manager, Location Manager, Store Manager, Shift Supervisor, Team Lead, Provost, Vice Provost, Chancellor, Vice Chancellor, Registrar, Bursar, Dean of Students, Associate Dean, Academic Dean, Dean of Instruction, Dean of Workforce Development, Director of Workforce Development, Director of Continuing Education, Department Chair, Program Chair, Professor, Associate Professor, Adjunct Professor, Lecturer, Superintendent, School Principal, Assistant Principal, CTE Director, CTE Coordinator, Board Member, Trustee, Instructor, Lead Instructor, Clinical Instructor, Driving Instructor, CDL Instructor, Welding Instructor, HVAC Instructor, Cosmetology Instructor, Barber Instructor, Massage Instructor, Certified Flight Instructor, CFI, Teacher, Educator, Trainer, Tutor, Admissions Representative, Admissions Advisor, Admissions Counselor, Admissions Coordinator, Enrollment Advisor, Enrollment Counselor, Enrollment Specialist, Student Services Coordinator, Student Success Coach, Career Services Coordinator, Job Placement Coordinator, Externship Coordinator, Financial Aid Officer, Financial Aid Advisor, Financial Aid Administrator, Compliance Officer, Director of Compliance, Director of Accreditation, Cosmetologist, Licensed Cosmetologist, Esthetician, Licensed Esthetician, Hair Stylist, Barber, Master Barber, Nail Technician, Massage Therapist, Licensed Massage Therapist, LMT, Dental Assistant, Registered Dental Assistant, Dental Hygienist, Phlebotomist, Medical Assistant, Certified Nursing Assistant, CNA, LPN, Registered Nurse, RN, Truck Driver, CDL Driver, Welder, Electrician, Plumber, HVAC Technician, Pilot, Tattoo Artist, Driver Recruiter, Fleet Manager, Terminal Manager, Dispatcher, CDL Examiner, Third Party Tester, assistant, associate, intern, trainee, apprentice, coordinator, specialist, technician, analyst, engineer, support, representative, rep, staff, clerk, logistics, shipping, warehouse, payroll, safety, quality, field, maintenance, territory, boutique, realtor, counselor, advisor, property, social media, web design, email marketing, SEO, PPC, ads manager, product owner, product manager, customer success, account management, regional, branch, district, area, zone, location, site, chapter, unit, junior, graduate, entry level, seasonal, temporary, contract, freelance, part-time, volunteer, shift, crew, floor, provost, chancellor, professor, adjunct, lecturer, faculty, superintendent, trustee, registrar, bursar, K-12, CTE, continuing education, workforce, examiner, tester, proctor, dispatch, recruiter, fleet, terminal, clinical, externship, tutor, teacher, substitute, librarian, coach
```

### 3.3 Matching rules (Claude Code must implement)

- **Keywords are whole-word or whole-phrase matches, case-insensitive.** "rep" must not match "Reporting", "unit" must not match "Community". Substring matching will kill buyers.
- **Add a unit test:** no title in 3.1 may match any entry in 3.2. This spec was checked with that test and passes.
- Practitioner and instructor roles are full titles, not keywords, because small-school owners write "Owner & Lead Instructor" or "Master Barber / Owner". A keyword block would remove real buyers. If a contact's title contains an include title, keep it even when it also contains an exclude title (for example "Owner / Lead Instructor").
- **Office Manager is deliberately not excluded.** At 11 to 20 person schools this person often runs admissions and scheduling. Treat them as a referral path, not a primary target.
- "dean" is not a keyword (a Dean of Admissions at a private career college can buy). "Program Director" is not excluded but is borderline in healthcare schools where it is an accreditation-required clinical role. "clinical" is a keyword, so review the first healthcare pulls for lost buyers.
- Franchise exclusions are removed except "Franchisor". Partner-brand beauty schools are often independently owned.
- **Where it runs:** AI.ARK contact search takes the include list, then apply the exclude list as a post-filter before `contact-qa`. Check whether the pipeline has a native exclude option. If not, write the filter as a small script and document it. (VERIFY-10)

## 4. Vertical to similar-school map

Every email closes on one low-friction CTA that names a Lumion school from the prospect's vertical. Save this block as `school-map.json`.

```json
{
  "_rule": "Names only. No metrics. Use status 'approved' or 'closest' only. For 'unapproved' or missing verticals use the fallback CTA.",
  "fallback_cta": "Want me to send over what the first 30 days looked like for a school doing your volume?",
  "cta_template": "Want me to send over what the first 30 days looked like for {similar_school}?",
  "verticals": {
    "coding_tech": {
      "school": "Tripleten",
      "alt": "Coding Temple",
      "status": "approved"
    },
    "cyber_security": {
      "school": "Iron Circle",
      "alt": null,
      "status": "approved"
    },
    "dental_assisting": {
      "school": "Berry Best Phlebotomy",
      "alt": null,
      "status": "closest"
    },
    "healthcare_vocational": {
      "school": "Berry Best Phlebotomy",
      "alt": null,
      "status": "approved"
    },
    "welding_ndt": {
      "school": "Arclabs Welding",
      "alt": null,
      "status": "approved"
    },
    "hvac_plumbing_electrical": {
      "school": "Hoosier Trade School",
      "alt": null,
      "status": "approved"
    },
    "massage_therapy": {
      "school": "Savant Aesthetics Institute",
      "alt": null,
      "status": "closest"
    },
    "cosmetology": {
      "school": "Savant Aesthetics Institute",
      "alt": null,
      "status": "approved"
    },
    "barbering": {
      "school": "Savant Aesthetics Institute",
      "alt": null,
      "status": "closest"
    },
    "tattoo_body_art": {
      "school": "Savant Aesthetics Institute",
      "alt": null,
      "status": "closest"
    },
    "cdl_trucking": {
      "school": "CDL Training of Tampa",
      "alt": "Dasmesh Truck Driving School",
      "status": "approved"
    },
    "heavy_equipment_crane": {
      "school": "Train For The Crane",
      "alt": null,
      "status": "approved"
    },
    "lineman_maritime_diving": {
      "school": "Train For The Crane",
      "alt": null,
      "status": "closest"
    },
    "flight_aviation_shelved": {
      "school": "RiseAero",
      "alt": "FlexAir",
      "status": "approved"
    },
    "mechatronics": {
      "school": "Mach 1 Mechatronics",
      "alt": null,
      "status": "unapproved"
    },
    "new_school": {
      "school": "Elite Career Institute",
      "alt": null,
      "status": "unapproved"
    }
  }
}
```

Rules: status `approved` and `closest` may be named. `unapproved` and missing verticals use the fallback CTA until Drew approves the name. Dental, massage, barbering, tattoo and the lineman group have no direct customer yet, so they use the closest school. Western Welding Academy and Avanti Beauty Academy are on the onboarding list and could become direct proof for welding and cosmetology once approved. (VERIFY-5)

**How Lumion fills seats** (use these as the mechanism lines in copy, one per email, never all five):

| Where seats leak | What Lumion does | Copy line |
| --- | --- | --- |
| Visitors leave without reaching out | Lead capture and dynamic enrollment forms | Lumion catches every visitor who shows interest on your site and starts the conversation by text in minutes. |
| Slow follow-up | Automated SMS follow-up and admissions CRM | Lumion texts every inquiry within minutes and keeps following up, so students hear from you before anyone else. |
| Calls after the office closes | Voice AI phone agent | Lumion answers every call in your school's voice, day or night, and books a real callback before they hang up. |
| Students quit mid-application | Mobile enrollment forms (VERIFY-1) | Lumion turns your application into a mobile form students can finish from their phone in one sitting. |
| Students cannot pay upfront | Payments | Lumion puts payment plans directly into your admissions flow so students see options instantly and say yes on the spot. |

## 5. Copy angles

Three angles that no campaign on record has used. Prior work leaned on speed to lead, payments first, the "fourth employee" framing, new-school audits and HubSpot displacement. Cross-check against the live EmailBison campaign list before building, because the project files may not show every campaign.

| # | Angle | Gap it fills | Best verticals |
| --- | --- | --- | --- |
| 1 | The PDF Application | Onboarding pain point 3 (application to enrollment drop-off), never built into a campaign | Dental, Cosmetology / Barbering, Massage |
| 2 | After 5PM | Voice AI has only been a CECU demo hook, never cold email | Welding, HVAC, CDL, Multi-Trade |
| 3 | Next Start Date | Seasonality was planned for Weeks 13+ in the March GTM Brief and never ran as a named angle | Coding / Cyber, Welding, Barbering |

**CTA standard for all three:** "Want me to send over what the first 30 days looked like for {similar_school}?" The fallback is in `school-map.json`. The CTA is a low-friction ask for information, not a meeting ask. The reply handler then moves interested replies toward a 15 minute slot with concrete times.

### 5.1 Angle 1: The PDF Application  ·  slug `pdf-application`  ·  prompt slot A (`research_emails_v1.md`)

**The bet:** Students quit mid-application when the only path is a PDF or a phone call, and no report shows it. A mobile application that saves progress and follows up by text recovers them.

**What proves it right:** Positive reply and meeting rate above the account's other angles on the same verticals at equal send volume (engineer sets the threshold after the first 300 sends).

**Best verticals:** Dental Assisting, Cosmetology and Barbering, Massage Therapy. Dental also carries the highest internal approval rate (11%), and a saved application gives the spouse conversation room.

**Signal fields (embed in company description text, see 6.4):**

| SIGNAL_APPLICATION_FORMAT | pdf | print_and_bring | call_to_schedule | online_form | none_found | Fetch the apply, enroll or admissions page. Flag links ending in .pdf, text such as download application or print, and tour-only or call-only entry points. |
| --- | --- | --- |
| SIGNAL_VERTICAL | key from school-map.json | From the directory category the school was sourced under. |

**Qualifies when:** SIGNAL_APPLICATION_FORMAT is pdf, print_and_bring or call_to_schedule.

**Reference Email 1** (423 characters, target 380 to 460). Replace `[School Name]` with a real sample prospect when writing `copy-previews/`.

```text
Noticed the enrollment application on [School Name]'s site is a PDF students print and bring in.

Someone applying to a dental assisting program is usually filling it out on their phone at 10pm. Lumion turns your application into a mobile form that saves their progress and texts them to finish, so more inquiries become enrolled students.

Want me to send over what the first 30 days looked like for Berry Best Phlebotomy?
```

**Reference Email 2** (604 characters, target 600 to 699)

```text
One more thought on the application piece.

When the only way to apply is a PDF, the students who quit halfway never show up anywhere. They don't call or email. They enroll at a school that let them finish on their phone.

Lumion swaps that PDF for a mobile application that saves progress, texts a reminder to anyone who stops partway, and drops every finished application into your admissions queue. Payment plans sit inside the same flow, so a student can pick one before they close the tab.

Berry Best Phlebotomy uses Lumion for enrollment. Want me to send over what their first 30 days looked like?
```

### 5.2 Angle 2: After 5PM  ·  slug `after-5pm`  ·  prompt slot A (`research_emails_v1.md`)

**The bet:** Prospects work day shifts and call after hours. A voice agent that answers, books a real callback and texts the application turns missed calls into booked callbacks.

**What proves it right:** Meeting rate on Welding, HVAC and CDL beats the same verticals on the account's existing angles. Voice AI is a June 2026 product and has only been used as a CECU conference demo hook, so this is its first cold email test.

**Best verticals:** Welding / NDT (9 day median close), HVAC / Plumbing / Electrical, CDL / Trucking, Multi-Trade.

**Signal fields (embed in company description text, see 6.4):**

| SIGNAL_OFFICE_CLOSE_TIME | HH:MM local, or none_found | Google Business Profile hours. Check what `googlemaps_discover.py` already returns before writing a new fetch. Fall back to the site footer. |
| --- | --- | --- |
| SIGNAL_WEEKEND_HOURS | open | closed | none_found | Same sources. |
| SIGNAL_VERTICAL | key from school-map.json | From the directory category. |

**Qualifies when:** SIGNAL_OFFICE_CLOSE_TIME is 18:00 or earlier, or SIGNAL_WEEKEND_HOURS is closed. The 18:00 cutoff is a proposal, engineer confirms.

**Gate before launch:** VERIFY-2 (is Voice AI sold standalone or bundled). If it is an add-on only, write the pricing deflection reply first. Pricing questions are deflected to a call, never answered with numbers.

**Reference Email 1** (420 characters, target 380 to 460). Replace `[School Name]` with a real sample prospect when writing `copy-previews/`.

```text
Your Google listing says the office at [School Name] closes at 5.

People looking at a welding program usually work a full shift and call on the way back from the job site. Lumion answers those calls in your school's voice, books a real callback, and texts the application while they're still on the line, so the call turns into a start date.

Want me to send over what the first 30 days looked like for Arclabs Welding?
```

**Reference Email 2** (619 characters, target 600 to 699)

```text
One more thought on the after hours calls.

Someone who calls a welding school at 7pm and hits voicemail rarely leaves a message. They call the next school on the list, and whoever picks up books the tour.

Lumion's phone agent answers every call in your school's voice, books a real callback, and texts the caller your application before they hang up. It remembers earlier texts, forms and calls from the same person, so nobody repeats themselves. Your team starts the morning with booked callbacks instead of missed calls.

Arclabs Welding works with Lumion. Want me to send over what their first 30 days looked like?
```

### 5.3 Angle 3: Next Start Date  ·  slug `next-start-date`  ·  prompt slot A (`research_emails_v1.md`)

**The bet:** A published start date makes the timing concrete, and the school's own unworked inquiries become the offer. Seasonality was planned in the March GTM Brief for Weeks 13 and later and has never run as a named angle.

**What proves it right:** Reply rate on records inside the 30 to 45 day window beats records outside it (engineer can split on `start_date_days_out`).

**Best verticals:** Coding / Cyber bootcamps (Tier A, cohort based), Welding / NDT, Barbering. Enrollment peaks are January and August/September, so the best send months are late October through November, and again in June and July.

**Signal fields (embed in company description text, see 6.4):**

| SIGNAL_NEXT_START_DATE | YYYY-MM-DD, or none_found | Scrape the next published start or cohort date from the program or calendar page. |
| --- | --- | --- |
| SIGNAL_PROGRAM_NAME | string | The program the date belongs to. |
| SIGNAL_VERTICAL | key from school-map.json | From the directory category. |

**Qualifies when:** SIGNAL_NEXT_START_DATE is 30 to 45 days after the planned send date. Rebuild this list on a rolling basis. A stale date makes the email wrong.

**Gate before launch:** VERIFY-3 (does Lumion text a school's backlog of older inquiries about an upcoming start date).

**Reference Email 1** (384 characters, target 380 to 460). Replace `[School Name]` with a real sample prospect when writing `copy-previews/`.

```text
Saw the next HVAC class at [School Name] starts January 12.

Schools usually have a pile of inquiries from the last 90 days that nobody reached twice. Lumion texts every one of them and puts payment plans right in the enrollment flow, so students say yes on the spot and fill the seats you still have.

Want me to send over what the first 30 days looked like for Hoosier Trade School?
```

**Reference Email 2** (609 characters, target 600 to 699)

```text
One more thought on the January class.

The quickest seats to fill belong to people who already asked about the program. Plenty of them went quiet after one call or one email because nobody followed up a second time. A short text is an easy way back into the conversation.

Lumion texts every inquiry from the last 90 days about the January 12 start and keeps following up until they apply or say no. When tuition is the holdup, payment plans sit right inside the enrollment flow so they can say yes on the spot.

Hoosier Trade School runs on Lumion. Want me to send over what their first 30 days looked like?
```

## 6. Build instructions

### 6.1 Execution lane

All three campaigns are **manual-prep**. The signal is the qualifier, so the list is built first and the run enters the pipeline at the `contacts` stage. Per the pipeline contract, manual-prep rides on top of the standard mix (2 to 3 Large TAM, 2 Lookalike, 2 to 3 High-Intent) and does not replace it. That slate is not defined in this spec. (VERIFY-11)

### 6.2 Package layout

```
lumion/
  SPEC.md                         (this file)
  strategy.json                   (all three campaigns, schema in 6.3)
  campaigns/01-pdf-application.json
  campaigns/02-after-5pm.json
  campaigns/03-next-start-date.json
  school-map.json                 (section 4)
  titles/include.txt  titles/exclude.txt
  prompts/<slug>/research_emails_v1.md     (one per campaign, slot A)
  copy-previews/0N-<slug>-drafts.md        (approved drafts, the quality bar)
  prospects/lumion/manual/<slug>-companies.csv
  run-commands.sh
```

### 6.3 strategy.json (schema from `gtm_strategy.py`)

Emit this as `strategy.json`, then split each campaign into its own file under `campaigns/`. Validate against the pipeline schema before use. `proof_anchor` has no number because no metric is approved, which is an intentional exception to the schema's usual quality rule.

```json
{
  "messaging_foundation": {
    "one_liner": "Lumion is the enrollment platform built for trade schools: it captures every inquiry, follows up by text within minutes, answers calls in the school's voice, and puts payment plans inside the admissions flow.",
    "core_problem": "Trade schools pay for traffic and calls that never become enrolled students because follow-up is slow, applications are manual, and students who cannot pay upfront are turned away.",
    "proof_anchor": "Name-only proof until Drew confirms 2025 Impact Report metrics. Approved names: Hoosier Trade School, Arclabs Welding, Berry Best Phlebotomy, Savant Aesthetics Institute, CDL Training of Tampa, Tripleten, Iron Circle. No numbers in copy."
  },
  "campaigns": [
    {
      "name": "Lumion - PDF Application",
      "campaign_type": "Large TAM",
      "target_persona": {
        "titles": [
          "Owner",
          "Co-Owner",
          "Owner/Operator",
          "Founder",
          "Co-Founder",
          "President",
          "CEO",
          "Chief Executive Officer",
          "Managing Director",
          "Executive Director",
          "School Director",
          "Campus Director",
          "Operator",
          "Director of Admissions",
          "Director of Enrollment",
          "Head of Admissions",
          "Head of Enrollment",
          "VP of Enrollment",
          "Director of Marketing",
          "Head of Marketing",
          "VP of Marketing",
          "COO",
          "Chief Operating Officer",
          "CFO",
          "Director of Finance"
        ],
        "seniority": "Owner / Director",
        "department": "Executive / Admissions"
      },
      "target_company": {
        "industries": [
          "Dental Assisting",
          "Cosmetology",
          "Barbering",
          "Massage Therapy"
        ],
        "size_range": "11-200",
        "geography": [
          "US"
        ],
        "signals": [
          "MANUAL-PREP: school's online application is a PDF, print and bring in, or call to schedule only (SIGNAL_APPLICATION_FORMAT)"
        ]
      },
      "messaging_angle": {
        "opening_hook": "Name the exact thing on their site: the application is a PDF students print and bring in.",
        "pain_hypothesis": "Students who start an application on their phone and cannot finish it never show up in any report, so the school loses them silently before a start date.",
        "poke_the_bear": "How many of the people who open your application ever finish it?",
        "best_case_study": "Per prospect from school-map.json by vertical (dental: Berry Best Phlebotomy, cosmetology and barbering: Savant Aesthetics Institute).",
        "proof_strategy": "School name only, in the CTA sentence. No metrics."
      },
      "search_parameters": {}
    },
    {
      "name": "Lumion - After 5PM",
      "campaign_type": "Large TAM",
      "target_persona": {
        "titles": [
          "Owner",
          "Co-Owner",
          "Owner/Operator",
          "Founder",
          "Co-Founder",
          "President",
          "CEO",
          "Chief Executive Officer",
          "Managing Director",
          "Executive Director",
          "School Director",
          "Campus Director",
          "Operator",
          "Director of Admissions",
          "Director of Enrollment",
          "Head of Admissions",
          "Head of Enrollment",
          "VP of Enrollment",
          "Director of Marketing",
          "Head of Marketing",
          "VP of Marketing",
          "COO",
          "Chief Operating Officer",
          "CFO",
          "Director of Finance"
        ],
        "seniority": "Owner / Director",
        "department": "Executive / Admissions"
      },
      "target_company": {
        "industries": [
          "Welding / NDT",
          "HVAC / Plumbing / Electrical",
          "CDL / Trucking",
          "Multi-Trade"
        ],
        "size_range": "11-200",
        "geography": [
          "US"
        ],
        "signals": [
          "MANUAL-PREP: office closes at or before 6:00 PM local or is closed on weekends (SIGNAL_OFFICE_CLOSE_TIME, SIGNAL_WEEKEND_HOURS)"
        ]
      },
      "messaging_angle": {
        "opening_hook": "Quote their own posted closing time back to them.",
        "pain_hypothesis": "Career changers work a full shift and call after the office closes, hit voicemail, and call the next school on the list.",
        "poke_the_bear": "What happens to a call that comes in at 7pm after your office closes?",
        "best_case_study": "Per prospect from school-map.json (welding: Arclabs Welding, HVAC and trades: Hoosier Trade School, CDL: CDL Training of Tampa).",
        "proof_strategy": "School name only, in the CTA sentence. No metrics."
      },
      "search_parameters": {}
    },
    {
      "name": "Lumion - Next Start Date",
      "campaign_type": "Large TAM",
      "target_persona": {
        "titles": [
          "Owner",
          "Co-Owner",
          "Owner/Operator",
          "Founder",
          "Co-Founder",
          "President",
          "CEO",
          "Chief Executive Officer",
          "Managing Director",
          "Executive Director",
          "School Director",
          "Campus Director",
          "Operator",
          "Director of Admissions",
          "Director of Enrollment",
          "Head of Admissions",
          "Head of Enrollment",
          "VP of Enrollment",
          "Director of Marketing",
          "Head of Marketing",
          "VP of Marketing",
          "COO",
          "Chief Operating Officer",
          "CFO",
          "Director of Finance"
        ],
        "seniority": "Owner / Director",
        "department": "Executive / Admissions"
      },
      "target_company": {
        "industries": [
          "Coding / Tech",
          "Cyber Security",
          "Welding / NDT",
          "Barbering"
        ],
        "size_range": "11-200",
        "geography": [
          "US"
        ],
        "signals": [
          "MANUAL-PREP: next published start or cohort date is 30 to 45 days out at send time (SIGNAL_NEXT_START_DATE, SIGNAL_PROGRAM_NAME)"
        ]
      },
      "messaging_angle": {
        "opening_hook": "Reference the specific class and start date published on their site.",
        "pain_hypothesis": "Inquiries from the last 90 days sit unworked while a start date approaches, and seats go unfilled that a second follow-up would have filled.",
        "poke_the_bear": "How many people who asked about your January class in the last 90 days have heard from you twice?",
        "best_case_study": "Per prospect from school-map.json (bootcamps: Tripleten or Iron Circle, welding: Arclabs Welding, barbering: Savant Aesthetics Institute).",
        "proof_strategy": "School name only, in the CTA sentence. No metrics."
      },
      "search_parameters": {}
    }
  ]
}
```

### 6.4 Company list CSV and signal embedding

For each campaign, build `prospects/lumion/manual/<slug>-companies.csv` with columns `company_name,domain,vertical,<signal columns>,similar_school`.

1. Take the school universe from regulatory directories (section 2), filter through the ICP gates, and assign `vertical`.
2. For each school, fetch the signal from the school's own site or Google Business Profile (tables in section 5). Write `none_found` rather than guessing. Drop rows that fail the angle's qualifier.
3. Set `similar_school` from `school-map.json`. Blank when the status is `unapproved` so the prompt uses the fallback CTA.
4. **Custom signals do not flow as merge tags.** Before the `contacts` stage, append them to the company description text as prefixed lines, for example `SIGNAL_APPLICATION_FORMAT: pdf` and `SIGNAL_SIMILAR_SCHOOL: Berry Best Phlebotomy`. The research prompt reads them from there.
5. Dedupe against domains already contacted in Lumion's EmailBison workspace and against the Do Not Contact list (none provided yet).

### 6.5 Prompt files

One `research_emails_v1.md` per campaign (slot A, v1 maps to A). B and C are reserved. Format per the pipeline contract:

- Exactly three fenced `json` blocks in order: Research, Email 1, Email 2. Each is a full request body with `model`, `messages` (system and user), `max_tokens`, `temperature`.
- Copy the user-block merge tags from an existing `research_emails_v*.md` in the repo. Do not invent tags. Known sets: Research uses `{{Company Name}} {{Domain}} {{Industry}} {{First Name}} {{Last Name}} {{Job Title}}` plus `{{LinkedIn Company Description}} {{Company Description}} {{Recent News}}`. Email 1 uses `{{Research Output}} {{Job Title}} {{Company Name}}`. Email 2 adds `{{Email 1 Output}}`.
- Use the current Sonnet writing model already used in the repo's prompts. Temperature 0.6 to 0.8 for emails, lower for research.
- **The files replace pipeline defaults entirely**, so each Email system prompt must embed the guardrail block below plus the client bans.
- Each Email system prompt runs 600 to 1,200 words and contains: role and sender identity (Drew Jones, Lumion); the angle's bet stated explicitly; the structure step by step with a character budget; 2 to 3 good examples (the reference drafts in section 5, lightly genericized) and 1 to 2 bad examples with the failure named; 8 to 15 buyer phrases from section 1 and the copy lines in section 4; the guardrail block; proof rules; output format rules.
- **Research prompt** extracts the SIGNAL lines, confirms the school passes the ICP gates, selects the approved `SIMILAR_SCHOOL` from the map embedded in the prompt (or `NONE`), and outputs a short brief. Embed the section 4 map directly in the prompt text.
- Email 1 length 380 to 460 characters. Email 2 length 600 to 699 characters. Tell the model both numbers.
- Proof rule: only school names from the map, no numbers, and when `SIMILAR_SCHOOL` is `NONE` use the fallback CTA verbatim.

**Guardrail block (embed verbatim in every Email prompt):**

```text
HARD CONSTRAINTS:
- Output ONLY the email body. No subject, greeting, name, signature, commentary, code fences,
  or character counts. First word of output = first word of the opening sentence.
- Email 1: 300-500 characters. Email 2: 600-800 characters. Count silently.
- Peer voice, not consultant: contractions everywhere, short plain sentences, warmth over
  authority, specific details over industry claims. If it reads like a LinkedIn post, rewrite.
- BANNED OPENERS: "Most [X] we talk to...", any "Most [X]..." generalization, stat/percentage
  openers, product-name openers, "Industry-wide...".
- BANNED VOCABULARY: hope this finds you well / just checking in / I wanted to reach out /
  quick call / hop on a call / leverage / optimize / streamline / synergy / pain points /
  value proposition / best practices / best-in-class / cutting-edge / just following up /
  circling back / bumping this / trusted by / limited time / 10x / skyrocket / transform.
- No colons in opening lines. No emojis. Max 1 exclamation point. Paragraphs 1-2 sentences
  with white space between. Exactly one CTA.
- Social proof: ONLY the approved case studies listed above, numbers verbatim. If none fits,
  write proof-free. Never invent or round numbers.
```

**Client specific bans to append:**

```text
- No pricing, packages or commercial terms. If asked, deflect to a call.
- No case study numbers or percentages. School names only.
- No dash characters of any kind in the email body.
- No loss framing such as "stop losing". Describe the outcome that becomes possible.
- No competitor names.
- Never claim a feature beyond the copy lines in the spec. Anything marked VERIFY stays in the wording of the reference drafts.
- Exactly one CTA, the similar-school question or its fallback.
- Retired jargon: platform, solution, ecosystem, seamless, AI-powered, end-to-end, funnel optimization.
```

### 6.6 Variant manifest

| Campaign | Slot | File | Variant name | The bet | Proves it right |
| --- | --- | --- | --- | --- | --- |
| 01 PDF Application | A | prompts/pdf-application/research_emails_v1.md | Name the PDF | Pointing at the exact PDF on their site earns more replies than a general speed claim | Reply and meeting rate vs other angles on the same verticals |
| 02 After 5PM | A | prompts/after-5pm/research_emails_v1.md | Quote the closing time | A school's own posted hours make the missed call real to the owner | Meeting rate on welding, HVAC, CDL |
| 03 Next Start Date | A | prompts/next-start-date/research_emails_v1.md | Date on the calendar | A named class and date turns a vague follow-up promise into a deadline | Reply rate inside vs outside the 30 to 45 day window |

Assignment: one variant per campaign, so no variant assignment flag is needed. Each pushed lead must carry `variant` as an EmailBison custom field.

## 7. Run order and commands

**Execution order:** 02 After 5PM first (Voice AI is the newest asset and welding has the fastest close), then 03 Next Start Date (time-boxed, schedule sends to the 30 to 45 day window), then 01 PDF Application. Reason and order are a proposal, the engineer can reorder.

**Preflight (first lines of `run-commands.sh`).** Stop if either fails and fix `pipeline/.env`. A failed preflight means silent data loss, not an error.

```bash
cd services/research/pipeline
python -c "import run_pipeline as rp; rp._get_pipeline_neo4j_driver().verify_connectivity(); print('neo4j OK')"
python -c "import config, postgres_leads as pgl; pgl._connect().close(); print('postgres OK')"
# STOP if either preflight line fails. Fix pipeline/.env first.
```

**Per campaign:**

1. **Prompt swap (always first):**
```bash
rm -f prompts/research_emails_v*.md
cp <package-path>/prompts/<campaign-slug>/research_emails_v*.md prompts/
```
2. **Build the list** (6.4) and write the CSV.
3. **Enter at the `contacts` stage** against the CSV domains, then run in this order: `contact-qa`, `waterfall`, `columns-sample`, `columns-full`, `push-emailbison`. The contract names these subcommands but not their flags. Run `python run_pipeline.py <subcommand> --help` for each one and finalize `run-commands.sh` with real flags. Always use `--use-prompts`, `--skip-qa` (campaigns were human-approved, the QA judge would cull them), `--max-records 50` and `--contacts-per-domain 3` on the first run.
4. **Sample gate:** `columns-sample` renders about 5 prospects across all variants and writes nothing downstream. Engineer reviews the company gate, title preview, waterfall and copy against `copy-previews/`. Do not scale until it passes.
5. **Push:** `push-emailbison --dry-run` first to confirm the target, then the real push with the custom-fields flag on (confirm its name with `--help`) so `variant`, `research_brief` and `tier` reach EmailBison. Always pass `--emailbison-workspace-name "Lumion"` and name campaigns `"Lumion - PDF Application"`, `"Lumion - After 5PM"`, `"Lumion - Next Start Date"`. Tier A (ICP score 70 or higher) only unless the engineer says otherwise.
6. **Scale run:** `--max-records 200`, `--contacts-per-domain 5`, `--no-gate`, only after the sample passes.

**Verify the EmailBison target:** `list-emailbison-campaigns --workspace-id <id> --search "Lumion"`.

**Known tool issues (budget for them):**
- `emailbison_view_lead_conversations` has a persistent server-side schema bug. Use manual screenshots to read reply content.
- EmailBison does not know when a lead books a meeting. That lives in Calendly. Tag at booking via webhook and filter re-engagement audiences by that tag, and cross-check Calendly directly before any send. Calendly setup was listed as "No" on the onboarding form, so confirm it before launch.
- When calling models through OpenRouter, set `"reasoning": {"enabled": false}` and raise `max_tokens`, or extended thinking can consume the whole budget and return null content.

## 8. Acceptance criteria

1. `strategy.json` and the three campaign files validate against the pipeline schema, and every `poke_the_bear` ends with `?`.
2. Title unit test passes: zero overlap between 3.1 and 3.2 under whole-word matching, and the filter removes known noise titles on a 50 contact sample.
3. Every CSV row passes the section 2 gates, has the angle's qualifier true, and carries `none_found` rather than a guess for missing signals.
4. Each prompt file has exactly three json blocks, no invented merge tags, the full guardrail block, and the school map.
5. On `columns-sample`: E1 380 to 460 characters, E2 600 to 699, no dashes, one CTA, school named only from the map, no numbers, and reads like the reference drafts.
6. Preflight passes and the sample run shows no `Graph context bind failed`, `Postgres company sync FAILED` or `skipped_no_company` lines.
7. In market (proposed, engineer confirms): after 500 sends per campaign, rotate the angle or variant if positive replies are below the account's current baseline. Baseline is not in the project files.

## 9. Open items and VERIFY list

| ID | Item | Why it matters | Owner |
| --- | --- | --- | --- |
| VERIFY-1 | Does Lumion's application form save progress and text a reminder to finish? | Angle 1 copy and the section 4 line. Project files only confirm dynamic enrollment forms and SMS follow-up. | Drew |
| VERIFY-2 | Is Voice AI sold standalone or bundled with Engagement? | Angle 2 needs a pricing deflection if it is an add-on. | Drew |
| VERIFY-3 | Can Lumion text a backlog of older inquiries about an upcoming start date? | Angle 3 mechanism. | Drew |
| VERIFY-4 | First 30 days write-up for each named school (setup steps and what changed in weeks 1 to 4, no numbers needed). | The CTA promises it. No reply handler can send it until it exists. | Drew |
| VERIFY-5 | Approve Mach 1 Mechatronics, Elite Career Institute, Western Welding Academy, Avanti Beauty Academy as nameable schools. | Rows marked unapproved use the fallback CTA. | Drew |
| VERIFY-6 | 2025 Impact Report and competitive matrix, promised in March 2026 and still not received. | Unlocks metric-backed proof. Ask again. | Drew |
| VERIFY-8 | EmailBison workspace name, sender inbox count, and capacity check. Capacity was not computed because inbox count is unknown. | Run commands and volume sizing. | Engineer |
| VERIFY-9 | Win rates may be referral biased and are not ACV weighted. | Vertical order in section 2 and send priority. | Engineer |
| VERIFY-10 | Does the pipeline support title exclusion natively, and what are the stage-wise subcommand flags and the custom-fields push flag? | Section 3.3 and section 7. | Claude Code |
| VERIFY-11 | The Large TAM, Lookalike and High-Intent slate that these manual-prep campaigns ride on top of. | Pipeline contract requires the standard mix. | Engineer |

## 10. Sources

- Lumion Onboarding Form, Airtable submission dated March 7, 2026 (Drew Jones): ICP, titles, industries, pain points, stack, trigger events.
- Lumion GTM Strategy Draft Brief, BuzzLead, March 2026: Phase I and II ICPs, signal plays, timeline.
- Vertical Win/Loss Analysis, 1,512 pipeline deals, March 2026: win rates, loss signatures, channel data.
- Lumion Research Overview: positioning and ICP inference.
- lumion-engagement-evolution.md, reconstructed from project chats March 16 to August 10, 2026: ICP gates, ruled out verticals, case study discipline, Voice AI, copy and tone rules, infrastructure notes.
- BuzzLead skills: gtm-project-architect (addendum template, pipeline contract, copy studio), job-title-skill (exclusion logic), spam-word-checker-en-ish (banned words), cold-email-copywriter (copy standards).
