import streamlit as st

from generator import generate_prd_with_retrieval, evaluate_prd
from retrieval import get_similar_prd_metas

st.set_page_config(page_title="PRD Generator", page_icon="📋", layout="wide")
st.title("PRD Generator")
st.caption("Powered by Claude — generates a structured PRD and scores it with an LLM-as-judge eval.")

idea = st.text_area(
    "Describe your product idea",
    placeholder="e.g. a tool that helps remote engineering teams run async standups via Slack",
    height=120,
)

if st.button("Generate PRD", type="primary", disabled=not idea.strip()):
    with st.spinner("Retrieving similar PRDs and generating…"):
        try:
            prd = generate_prd_with_retrieval(idea.strip())
            retrieved_prds = get_similar_prd_metas(idea.strip(), k=2)
        except Exception as e:
            st.error(f"PRD generation failed: {e}")
            st.stop()

    with st.spinner("Running LLM-as-judge evaluation…"):
        try:
            evaluation = evaluate_prd(prd)
        except Exception as e:
            st.error(f"Evaluation failed: {e}")
            st.stop()

    st.session_state["prd"] = prd
    st.session_state["retrieved_prds"] = retrieved_prds
    st.session_state["evaluation"] = evaluation

if "retrieved_prds" in st.session_state:
    with st.expander("Retrieved similar PRDs (RAG context)"):
        for r in st.session_state["retrieved_prds"]:
            st.markdown(f"**{r['title']}**")
            sentences = r.get("problem_statement", "").split(". ")
            summary = ". ".join(sentences[:2]) + ("." if len(sentences) > 2 else "")
            st.caption(summary)

if "prd" in st.session_state:
    prd = st.session_state["prd"]
    evaluation = st.session_state["evaluation"]

    st.divider()
    st.header(prd.get("title", "Untitled"))

    st.subheader("Problem Statement")
    st.write(prd.get("problem_statement", ""))

    st.subheader("Target Users")
    for user in prd.get("target_users", []):
        st.markdown(f"- {user}")

    st.subheader("User Stories")
    for i, story in enumerate(prd.get("user_stories", []), 1):
        st.markdown(f"{i}. {story}")

    st.subheader("Acceptance Criteria")
    for criterion in prd.get("acceptance_criteria", []):
        st.markdown(f"- {criterion}")

    st.subheader("Success Metrics")
    metrics = prd.get("success_metrics", [])
    if metrics:
        cols = st.columns(3)
        cols[0].markdown("**Metric**")
        cols[1].markdown("**Baseline**")
        cols[2].markdown("**Target**")
        for m in metrics:
            c1, c2, c3 = st.columns(3)
            c1.write(m.get("metric", ""))
            c2.write(m.get("baseline", ""))
            c3.write(m.get("target", ""))

    st.subheader("Risks & Open Questions")
    for risk in prd.get("risks_open_questions", []):
        st.markdown(f"- {risk}")

    st.subheader("Out of Scope")
    for item in prd.get("out_of_scope", []):
        st.markdown(f"- {item}")

    st.divider()
    st.header("Eval Results")

    overall = evaluation.get("overall_score", 0)
    color = "green" if overall >= 7.5 else "orange" if overall >= 5.0 else "red"

    st.markdown(
        f"<h2 style='color:{color}'>Overall Score: {overall} / 10</h2>",
        unsafe_allow_html=True,
    )

    DIMENSIONS = ["specificity", "measurability", "testability", "user_centricity", "completeness"]
    scores = evaluation.get("scores", {})
    dim_cols = st.columns(5)
    for col, dim in zip(dim_cols, DIMENSIONS):
        entry = scores.get(dim, {})
        score = entry.get("score", "—")
        reason = entry.get("reason", "")
        col.metric(label=dim.replace("_", " ").title(), value=f"{score} / 10")
        col.caption(reason)

    st.subheader("Top 3 Improvements")
    for i, tip in enumerate(evaluation.get("top_3_improvements", []), 1):
        st.markdown(f"{i}. {tip}")
