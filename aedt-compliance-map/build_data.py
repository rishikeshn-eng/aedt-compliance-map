"""
Builds the regime dataset. Edit here, not the CSV, because cells contain
commas and hand-editing CSV breaks quoting.

Run: python build_data.py
"""
import csv
from pathlib import Path

DATA = Path(__file__).parent / "data"

REGIMES_HEADER = [
    "regime", "jurisdiction", "status", "in_force", "triggers",
    "audit_mandated", "notice_required", "publication_required",
    "penalties", "who_is_liable", "notes",
]

REGIMES = [
    ["NYC Local Law 144 (AEDT Law)", "New York City", "In force", "2023-07-05",
     "Using an automated employment decision tool to substantially assist screening of candidates for NYC-based roles, including by remote employers",
     "Yes — independent annual bias audit, named in statute", "Yes — 10 business days advance notice to candidates",
     "Yes — audit results published on the employer website",
     "USD 500 to 1,500 per violation per day",
     "Employer or employment agency",
     "The only regime that mandates an independent bias audit by name. A vendor's own bias report does not satisfy it."],

    ["California CRC automated-decision-system regs (FEHA)", "California", "In force", "2025-10-01",
     "Using an automated decision system in employment decisions affecting California workers",
     "No mandate, but an independent audit is the strongest evidentiary defence", "Transparency duties arise under CCPA",
     "No",
     "FEHA discrimination exposure",
     "Employer; vendors exposed via aiding-and-abetting and agent theories",
     "Using a biased tool is not a defence to a discrimination claim. Mobley v. Workday foregrounded vendor exposure."],

    ["Illinois HB 3773 (amends Human Rights Act)", "Illinois", "In force", "2026-01-01",
     "Using AI that has the effect of discriminating in recruitment, hiring, promotion or discipline",
     "No", "Yes — notice to applicants", "No",
     "Illinois Human Rights Act remedies",
     "Employer",
     "Regulates employers directly, structurally closer to LL144 than to Colorado. No audit or publication mandate."],

    ["Illinois AI Video Interview Act", "Illinois", "In force", "2020-01-01",
     "Using AI to analyse video interviews for Illinois positions",
     "No", "Yes — consent and explanation required before use", "No",
     "Statutory obligations; limited private remedy",
     "Employer",
     "Predates the current wave. Often missed because it is narrow and old."],

    ["Texas Responsible AI Governance Act", "Texas", "In force", "2026-01-01",
     "Developing or deploying AI systems in Texas, with intent-based discrimination provisions",
     "No", "Varies by provision", "No",
     "Attorney General enforcement",
     "Developers and deployers",
     "Intent-based rather than disparate-impact based, which is a meaningfully different standard."],

    ["Colorado AI Act (SB 24-205, as amended)", "Colorado", "Delayed", "2027-01-01",
     "Deploying a high-risk AI system making or substantially factoring into a consequential employment decision",
     "No audit mandate, but impact assessments required", "Yes — notice to consumers", "No",
     "Deceptive trade practice under the Colorado Consumer Protection Act",
     "Developers and deployers, duty of reasonable care",
     "Effective date has moved more than once. Sources conflict; verify the current date before relying on it."],

    ["EU AI Act — employment as high-risk (Annex III)", "European Union", "Delayed", "2027-12-02",
     "Placing on the EU market or using an AI system for recruitment, selection, promotion or termination",
     "Conformity assessment required rather than a bias audit per se", "Yes — Article 50 transparency duties already apply from Aug 2026", "No",
     "Up to 7 percent of global turnover for prohibited practices; lower tiers for other breaches",
     "Providers and deployers",
     "High-risk obligations moved from 2 Aug 2026 to 2 Dec 2027 under the Digital Omnibus (Reg. 2026/1744)."],

    ["Title VII / ADA / ADEA (federal US)", "United States (federal)", "In force", "Long-standing",
     "Any employment practice with discriminatory effect, regardless of whether AI is involved",
     "No", "No", "No",
     "Federal discrimination remedies",
     "Employer",
     "Applies exactly as before. EEOC AI-specific technical assistance was removed from its website in early 2025, but the underlying statutes are unchanged."],

    ["Maryland HB 1202", "Maryland", "In force", "2020-10-01",
     "Using facial recognition during pre-employment interviews",
     "No", "Yes — consent required", "No",
     "Statutory",
     "Employer",
     "Very narrow scope: facial recognition only."],
]

CHECKS_HEADER = ["question", "key", "help"]
CHECKS = [
    ["Do you use any automated tool to screen, rank, or score job candidates?", "uses_aedt",
     "Includes resume parsers that rank, scoring models, and LLM-based screening. Tools that only store or format applications generally do not count."],
    ["Does the tool substantially assist or replace human decision-making?", "substantial",
     "The NYC threshold. A tool whose output a human relies on heavily counts, even if a person signs off."],
    ["Do you hire for roles based in New York City, including remote roles?", "nyc", ""],
    ["Do you hire workers in California?", "ca", ""],
    ["Do you hire workers in Illinois?", "il", ""],
    ["Do you use AI to analyse recorded video interviews?", "video", ""],
    ["Do you hire workers in Colorado?", "co", ""],
    ["Do you hire workers in Texas?", "tx", ""],
    ["Do you place the tool on the EU market, or use it for EU-based roles?", "eu", ""],
    ["Do you use facial recognition in interviews?", "face", ""],
]

SOURCES_HEADER = ["topic", "source", "url"]
SOURCES = [
    ["NYC LL144", "NYC Department of Consumer and Worker Protection, AEDT final rule", "https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page"],
    ["EU AI Act", "European Commission, regulatory framework for AI", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"],
    ["EU AI Act text", "Regulation (EU) 2024/1689, EUR-Lex", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"],
    ["Colorado", "Colorado General Assembly, SB 24-205", "https://leg.colorado.gov"],
    ["Illinois", "Illinois General Assembly, HB 3773", "https://www.ilga.gov"],
    ["California", "California Civil Rights Department", "https://calcivilrights.ca.gov"],
    ["Federal US", "EEOC", "https://www.eeoc.gov"],
    ["Four-fifths rule", "Uniform Guidelines on Employee Selection Procedures, 29 CFR 1607", "https://www.ecfr.gov"],
]


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {path.name}")


if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)
    write(DATA / "regimes.csv", REGIMES_HEADER, REGIMES)
    write(DATA / "triage_questions.csv", CHECKS_HEADER, CHECKS)
    write(DATA / "sources.csv", SOURCES_HEADER, SOURCES)
