"""
AI Hiring Compliance Map.

Educational triage over the regimes that apply to automated employment
decision tools. Not legal advice, and the app says so throughout.

Run:    streamlit run app.py
Deploy: see README.md
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AI Hiring Compliance Map", layout="wide")

DATA = Path(__file__).parent / "data"

# which triage keys switch on which regime
TRIGGER_MAP = {
    "NYC Local Law 144 (AEDT Law)": ["uses_aedt", "substantial", "nyc"],
    "California CRC automated-decision-system regs (FEHA)": ["uses_aedt", "ca"],
    "Illinois HB 3773 (amends Human Rights Act)": ["uses_aedt", "il"],
    "Illinois AI Video Interview Act": ["video", "il"],
    "Texas Responsible AI Governance Act": ["uses_aedt", "tx"],
    "Colorado AI Act (SB 24-205, as amended)": ["uses_aedt", "substantial", "co"],
    "EU AI Act — employment as high-risk (Annex III)": ["uses_aedt", "eu"],
    "Title VII / ADA / ADEA (federal US)": ["uses_aedt"],
    "Maryland HB 1202": ["face"],
}


@st.cache_data
def load():
    return (pd.read_csv(DATA / "regimes.csv"),
            pd.read_csv(DATA / "triage_questions.csv"),
            pd.read_csv(DATA / "sources.csv"))


regimes, questions, sources = load()

st.title("AI Hiring Compliance Map")
st.caption(
    "Which rules apply when you use AI to screen candidates, and which are "
    "actually in force. Compiled September 2026."
)
st.warning(
    "**Not legal advice.** This is an educational triage tool built from public "
    "sources. Effective dates in this area move frequently and sources disagree. "
    "Verify against the primary sources listed under Sources, and consult a "
    "qualified lawyer before relying on any of it.",
    icon="⚠️",
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Triage", "All regimes", "Timeline", "Sources"]
)

# ---------------- Triage ----------------
with tab1:
    st.subheader("Answer these to see which regimes likely apply")
    answers = {}
    cols = st.columns(2)
    for i, row in questions.iterrows():
        with cols[i % 2]:
            answers[row["key"]] = st.checkbox(
                row["question"],
                help=row["help"] if isinstance(row["help"], str) and row["help"] else None,
            )

    st.divider()
    applicable = [
        name for name, keys in TRIGGER_MAP.items()
        if all(answers.get(k, False) for k in keys)
    ]

    if not any(answers.values()):
        st.info("Tick the boxes above to run the triage.")
    elif not applicable:
        st.success("No regime in this dataset is clearly triggered by those answers.")
        st.caption(
            "That is not the same as 'no obligations'. This dataset covers nine "
            "regimes; more than two dozen US states have active AI hiring bills."
        )
    else:
        hits = regimes[regimes["regime"].isin(applicable)]
        in_force = hits[hits["status"] == "In force"]
        upcoming = hits[hits["status"] != "In force"]

        c1, c2, c3 = st.columns(3)
        c1.metric("Regimes triggered", len(hits))
        c2.metric("In force now", len(in_force))
        c3.metric("Audit mandated", int(hits["audit_mandated"].str.startswith("Yes").sum()))

        if len(in_force):
            st.markdown("### In force now")
            for _, r in in_force.iterrows():
                with st.expander(f"**{r['regime']}** — {r['jurisdiction']} (since {r['in_force']})"):
                    st.markdown(f"**Triggered by:** {r['triggers']}")
                    a, b = st.columns(2)
                    a.markdown(f"**Bias audit:** {r['audit_mandated']}")
                    a.markdown(f"**Candidate notice:** {r['notice_required']}")
                    b.markdown(f"**Publication:** {r['publication_required']}")
                    b.markdown(f"**Who is liable:** {r['who_is_liable']}")
                    st.markdown(f"**Penalties:** {r['penalties']}")
                    if isinstance(r["notes"], str) and r["notes"]:
                        st.info(r["notes"])

        if len(upcoming):
            st.markdown("### Not yet in force")
            for _, r in upcoming.iterrows():
                with st.expander(f"**{r['regime']}** — {r['jurisdiction']} (from {r['in_force']})"):
                    st.markdown(f"**Triggered by:** {r['triggers']}")
                    st.markdown(f"**Bias audit:** {r['audit_mandated']}")
                    if isinstance(r["notes"], str) and r["notes"]:
                        st.info(r["notes"])

        if any("Yes" in str(v) for v in hits["audit_mandated"]):
            st.success(
                "**Practical note:** where several regimes apply, a single independent "
                "bias audit built to NYC LL144 standards (sex and race/ethnicity at "
                "minimum, intersectional analysis, four-fifths threshold) generally "
                "serves as the evidentiary floor across the others, even where they "
                "do not mandate an audit by name."
            )

# ---------------- All regimes ----------------
with tab2:
    st.subheader("Every regime in the dataset")
    status_filter = st.multiselect("Status", regimes["status"].unique(),
                                   default=list(regimes["status"].unique()))
    view = regimes[regimes["status"].isin(status_filter)]
    st.dataframe(
        view[["regime", "jurisdiction", "status", "in_force",
              "audit_mandated", "notice_required", "penalties"]],
        width="stretch", hide_index=True,
    )
    st.markdown("### Read one in full")
    pick = st.selectbox("Regime", view["regime"].tolist())
    r = regimes[regimes["regime"] == pick].iloc[0]
    for label, key in [("Triggered by", "triggers"), ("Bias audit", "audit_mandated"),
                       ("Candidate notice", "notice_required"),
                       ("Publication", "publication_required"),
                       ("Penalties", "penalties"), ("Who is liable", "who_is_liable")]:
        st.markdown(f"**{label}:** {r[key]}")
    if isinstance(r["notes"], str) and r["notes"]:
        st.info(r["notes"])

# ---------------- Timeline ----------------
with tab3:
    st.subheader("What is actually in force, and when")
    st.write(
        "The gap between what people cite and what binds is the interesting part. "
        "The two most-discussed regimes, Colorado and the EU AI Act's high-risk "
        "rules for hiring, are both still pending."
    )
    tl = regimes.copy()
    tl["date_sort"] = pd.to_datetime(tl["in_force"], errors="coerce")
    tl = tl.dropna(subset=["date_sort"]).sort_values("date_sort")
    fig = px.scatter(
        tl, x="date_sort", y="regime", color="status",
        color_discrete_map={"In force": "#1F3A5F", "Delayed": "#C00000"},
        height=max(360, 42 * len(tl)),
        labels={"date_sort": "Effective date", "regime": ""},
    )
    fig.add_vline(x=pd.Timestamp.today(), line_dash="dash", line_color="grey")
    fig.update_traces(marker=dict(size=13))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), legend_title_text="")
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Dashed line is today. Long-standing federal statutes are excluded from "
        "this chart because they have no single effective date."
    )

# ---------------- Sources ----------------
with tab4:
    st.subheader("Sources")
    st.dataframe(sources, width="stretch", hide_index=True,
                 column_config={"url": st.column_config.LinkColumn("Link")})
    st.markdown("### Known limitations")
    st.markdown(
        "- Colorado's effective date has moved more than once and public sources "
        "disagree on the current one. Verify directly before relying on it.\n"
        "- The triage logic is a simplification. Real applicability turns on "
        "facts this tool does not ask about, such as employee headcount, "
        "the degree of human review, and how the tool is used.\n"
        "- Coverage is nine regimes. More than two dozen US states have active "
        "AI hiring bills, so absence from this list means nothing.\n"
        "- Nothing here is legal advice."
    )

st.divider()
st.caption("Built by Rishikesh Nair · Data and methodology open in the repo")
