"""
Streamlit UI for AutoResearchAI.

A modern, minimal interface for the LangGraph multi-agent research workflow.
"""

from __future__ import annotations

import time
from typing import Any

import streamlit as st

from config import GROK_MODEL
from graph.workflow import workflow
from memory.chroma import memory


STAGES = [
    "Planner",
    "Research",
    "Scraper",
    "Writer",
    "Reviewer",
]


st.set_page_config(
    page_title="AutoResearchAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-1: #080b14;
    --bg-2: #111827;
    --card: rgba(255, 255, 255, 0.075);
    --card-border: rgba(255, 255, 255, 0.14);
    --text-muted: rgba(229, 231, 235, 0.72);
    --accent: #8b5cf6;
    --accent-2: #06b6d4;
    --success: #34d399;
    --warning: #fbbf24;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(139, 92, 246, 0.28), transparent 32rem),
        radial-gradient(circle at top right, rgba(6, 182, 212, 0.20), transparent 28rem),
        linear-gradient(135deg, var(--bg-1), var(--bg-2));
    color: #f9fafb;
}

[data-testid="stSidebar"] {
    background: rgba(5, 8, 18, 0.72);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

.hero {
    padding: 2.2rem;
    border: 1px solid var(--card-border);
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.11), rgba(255,255,255,0.045));
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.32);
    backdrop-filter: blur(18px);
    margin-bottom: 1.4rem;
}

.hero h1 {
    font-size: clamp(2.2rem, 5vw, 4.6rem);
    line-height: 1;
    margin: 0 0 0.75rem 0;
    letter-spacing: -0.055em;
    font-weight: 800;
}

.gradient-text {
    background: linear-gradient(90deg, #ffffff, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: var(--text-muted);
    font-size: 1.08rem;
    max-width: 850px;
}

.glass-card {
    padding: 1.2rem;
    border-radius: 22px;
    border: 1px solid var(--card-border);
    background: var(--card);
    backdrop-filter: blur(16px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.22);
    margin-bottom: 1rem;
}

.stage-pill {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    margin-bottom: 0.65rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.055);
}

.status-waiting { color: rgba(229,231,235,0.62); }
.status-running { color: var(--warning); }
.status-completed { color: var(--success); }
.status-failed { color: #fb7185; }

.source-card {
    padding: 1rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.05);
    margin-bottom: 0.8rem;
}

.small-muted {
    color: var(--text-muted);
    font-size: 0.92rem;
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    border: 0;
    padding: 0.85rem 1.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    color: white;
    box-shadow: 0 14px 34px rgba(59, 130, 246, 0.28);
}

.stTextArea textarea {
    border-radius: 18px !important;
    background: rgba(255,255,255,0.07) !important;
    color: #f9fafb !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

[data-testid="stMetricValue"] {
    font-weight: 800;
}
</style>
"""


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def build_initial_state(query: str) -> dict[str, Any]:
    """Create the shared LangGraph state without changing its structure."""

    return {
        "query": query,
        "planner": {},
        "research": {
            "sources": [],
            "documents": [],
            "total_sources": 0,
        },
        "writer": {
            "report": "",
        },
        "review": {
            "score": 0,
            "approved": False,
            "feedback": "",
        },
        "iteration": 0,
        "runtime": 0.0,
    }


def get_memory_count() -> int:
    """Return memory count safely for the UI."""

    try:
        return memory.count()
    except Exception:
        return 0


def run_research(query: str) -> dict[str, Any]:
    """Run the existing LangGraph workflow and store scraped documents."""

    state = build_initial_state(query)
    start_time = time.perf_counter()
    final_state = workflow.invoke(state)
    final_state["runtime"] = round(time.perf_counter() - start_time, 2)

    documents = final_state.get("research", {}).get("documents", [])
    if documents:
        memory.store_documents(query=query, documents=documents)

    return final_state


def render_stage_timeline(statuses: dict[str, str]) -> None:
    """Render progress timeline cards."""

    icons = {
        "Waiting": "○",
        "Running": "●",
        "Completed": "✓",
        "Failed": "×",
    }

    for stage in STAGES:
        status = statuses.get(stage, "Waiting")
        css_class = f"status-{status.lower()}"
        st.markdown(
            f"""
            <div class="stage-pill">
                <strong>{stage}</strong>
                <span class="{css_class}">{icons.get(status, '○')} {status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sources(sources: list[dict[str, Any]]) -> None:
    """Render expandable source cards."""

    if not sources:
        st.info("No sources were collected yet.")
        return

    for index, source in enumerate(sources, start=1):
        title = source.get("title", "Untitled")
        url = source.get("url", "")
        snippet = source.get("snippet", "No snippet available.")

        with st.expander(f"{index}. {title}"):
            st.markdown(
                f"""
                <div class="source-card">
                    <p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>
                    <p class="small-muted">{snippet}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


with st.sidebar:
    st.markdown("## 🤖 AutoResearchAI")
    st.caption("LangGraph Multi-Agent Research Assistant")
    st.divider()
    st.markdown("### Project")
    st.write("Built for NTCC internship, research writing, GitHub portfolio, and resume demonstration.")
    st.markdown("### Model")
    st.code(GROK_MODEL)
    st.markdown("### Memory")
    st.metric("Stored Documents", get_memory_count())
    if "last_runtime" in st.session_state:
        st.metric("Last Runtime", f"{st.session_state.last_runtime}s")
    st.divider()
    st.markdown("### Pipeline")
    st.write("Planner → Research → Scraper → Writer → Reviewer")


st.markdown(
    """
    <div class="hero">
        <h1><span class="gradient-text">AutoResearchAI</span></h1>
        <p class="subtitle">
            A LangGraph-powered multi-agent research assistant that plans, searches,
            scrapes, writes, reviews, and improves structured research reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.25, 0.75], gap="large")

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    query = st.text_area(
        "Research topic",
        placeholder="Example: Applications of Generative AI in Healthcare",
        height=140,
    )
    start = st.button("Start Research", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Progress Timeline")
    timeline_placeholder = st.empty()
    with timeline_placeholder.container():
        render_stage_timeline(st.session_state.get("stage_statuses", {}))
    st.markdown('</div>', unsafe_allow_html=True)


if start:
    if not query.strip():
        st.warning("Please enter a research topic before starting.")
    else:
        running_status = {stage: "Running" for stage in STAGES}
        st.session_state.stage_statuses = running_status
        with timeline_placeholder.container():
            render_stage_timeline(running_status)

        try:
            with st.spinner("Agents are collaborating on your research report..."):
                result = run_research(query.strip())
            st.session_state.result = result
            st.session_state.last_runtime = result.get("runtime", 0.0)
            st.session_state.stage_statuses = {stage: "Completed" for stage in STAGES}
            st.success("Research workflow completed.")
        except Exception as exc:
            st.session_state.stage_statuses = {stage: "Failed" for stage in STAGES}
            st.error(f"Research workflow failed: {exc}")

        with timeline_placeholder.container():
            render_stage_timeline(st.session_state.stage_statuses)


result = st.session_state.get("result")

if result:
    research = result.get("research", {})
    review = result.get("review", {})
    report = result.get("writer", {}).get("report", "")
    sources = research.get("sources", [])
    documents = research.get("documents", [])
    runtime = result.get("runtime", 0.0)

    st.markdown("### Research Metrics")
    metric_cols = st.columns(5)
    metric_cols[0].metric("Research Score", review.get("score", 0))
    metric_cols[1].metric("Sources Found", research.get("total_sources", len(sources)))
    metric_cols[2].metric("Documents Scraped", len(documents))
    metric_cols[3].metric("Execution Time", f"{runtime}s")
    metric_cols[4].metric("Memory Count", get_memory_count())

    report_col, review_col = st.columns([1.35, 0.65], gap="large")

    with report_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## Final Report")
        st.markdown(report or "No report generated.")
        st.download_button(
            "Download Markdown",
            data=report,
            file_name="autoresearch_report.md",
            mime="text/markdown",
        )
        st.download_button(
            "Download TXT",
            data=report,
            file_name="autoresearch_report.txt",
            mime="text/plain",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with review_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("## Reviewer Panel")
        st.metric("Score", review.get("score", 0))
        st.metric("Approved", "Yes" if review.get("approved") else "No")
        st.markdown("### Feedback")
        st.write(review.get("feedback", "No feedback available."))
        weaknesses = review.get("weaknesses", [])
        if weaknesses:
            st.markdown("### Weaknesses")
            for weakness in weaknesses:
                st.write(f"- {weakness}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## Sources")
    render_sources(sources)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="glass-card">
            <h3>Ready when you are</h3>
            <p class="small-muted">
                Enter a topic and start the workflow. The agents will plan the research,
                collect sources, scrape documents, write a report, and review the result.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
