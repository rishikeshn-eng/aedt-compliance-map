

**Live app:** https://aedt-compliance-map.streamlit.app# aedt-compliance-map

> All code and data live in the [`aedt-compliance-map/`](aedt-compliance-map/) folder. Run `cd aedt-compliance-map` before the commands below. When deploying on Streamlit Community Cloud, set the main file path to `aedt-compliance-map/app.py`.

Which rules actually apply when a company uses AI to screen job candidates,
and which of them are genuinely in force right now.

No API key. No GPU. Streamlit plus a curated dataset, so it deploys free and
gives you a live public link.

## Why this exists

The gap between what gets cited and what actually binds is large in this
area. The two most-discussed regimes are the Colorado AI Act and the EU AI
Act's high-risk rules for hiring, and as of September 2026 **neither is in
force**. Colorado was amended and pushed back; the EU's high-risk
obligations for employment systems moved from August 2026 to December 2027
under the Digital Omnibus.

Meanwhile the regimes that do bind are less discussed: NYC Local Law 144
(since July 2023), California's Civil Rights Council ADS regulations under
FEHA (October 2025), Illinois HB 3773 (January 2026), the Texas Responsible
AI Governance Act (January 2026), and the Illinois AI Video Interview Act,
which has applied since 2020 and is routinely overlooked.

## What's in it

**Triage** — ten yes/no questions about your hiring setup, returning the
regimes likely triggered, split into in-force and pending, each with its
audit, notice, publication, penalty, and liability position.

**All regimes** — the full dataset, filterable, with a detail view.

**Timeline** — effective dates plotted against today, which makes the
in-force vs. pending split immediately visible.

**Sources** — primary sources for every claim, plus stated limitations.

## Setup and run

```bash
pip install -r requirements.txt
python build_data.py        # regenerates the CSVs
streamlit run app.py
```

Click through all four tabs and run a triage locally before deploying.

## Deploy free

1. Push this folder to its own public GitHub repo.
2. Go to **share.streamlit.io**, sign in with GitHub.
3. **New app** → your repo → branch `main` → main file `app.py` → Deploy.
4. You get a URL like `https://your-app.streamlit.app`. Put that on your
   resume, not the repo link.

Every `git push` redeploys automatically.

## Editing the data

Edit `build_data.py`, not the CSVs. Cells contain commas and hand-editing
CSV breaks the quoting. Then run `python build_data.py`.

Do not add a row without a source you actually read.

## Honest limitations, also stated inside the app

- **Not legal advice.** Educational triage built from public sources.
- Colorado's effective date has moved more than once and public sources
  disagree on the current one. Verify before relying on it.
- The triage logic is a simplification. Real applicability turns on facts
  this tool does not ask about: headcount, degree of human review, how the
  tool's output is used.
- Nine regimes covered. More than two dozen US states have active AI hiring
  bills, so absence from this list means nothing.
- Effective dates in this area change frequently. Check the date stamps.

## Extending it

- Add the pending state bills as a separate "watch" layer
- Add an obligations checklist export for a given triage result
- Add EU member-state implementation detail once national rules land
- Track changes over time so the app shows movement, not a snapshot
