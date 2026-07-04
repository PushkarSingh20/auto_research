"""
LangGraph Workflow

Connects all AI agents into a complete
research pipeline.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState

from agents.planner import planner_node
from agents.research_agent import research_node
from agents.scraper_agent import scraper_node
from agents.writer_agent import writer_node
from agents.reviewer_agent import reviewer_node


# ------------------------------------------------------------------
# Conditional Routing
# ------------------------------------------------------------------

MAX_ITERATIONS = 3
PASSING_SCORE = 8.5


def review_router(state: ResearchState) -> str:
    """
    Decide whether to continue improving the report
    or finish the workflow.
    """

    score = state.get("review", {}).get("score", 0)

    iteration = state.get("iteration", 0)

    if score >= PASSING_SCORE:
        return "end"

    if iteration >= MAX_ITERATIONS:
        return "end"

    state["iteration"] = iteration + 1

    return "rewrite"


# ------------------------------------------------------------------
# Build Workflow
# ------------------------------------------------------------------

builder = StateGraph(ResearchState)

builder.add_node("planner", planner_node)

builder.add_node("research", research_node)

builder.add_node("scraper", scraper_node)

builder.add_node("writer", writer_node)

builder.add_node("reviewer", reviewer_node)


# ------------------------------------------------------------------
# Edges
# ------------------------------------------------------------------

builder.add_edge(START, "planner")

builder.add_edge("planner", "research")

builder.add_edge("research", "scraper")

builder.add_edge("scraper", "writer")

builder.add_edge("writer", "reviewer")


builder.add_conditional_edges(
    "reviewer",
    review_router,
    {
        "rewrite": "writer",
        "end": END,
    },
)

workflow = builder.compile()