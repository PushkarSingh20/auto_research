"""
Planner Agent

Analyzes the user's query and creates a structured research plan.
"""

from __future__ import annotations

from graph.state import ResearchState
from prompts.planner_prompt import PLANNER_SYSTEM_PROMPT
from tools.llm import llm


def planner_node(state: ResearchState) -> ResearchState:
    """
    LangGraph Planner Node.

    Responsibilities:
    - Analyze query complexity
    - Generate research keywords
    - Decide number of sources
    - Create report outline

    Returns:
        Updated ResearchState
    """

    query = state["query"]

    user_prompt = f"""
User Query:

{query}

Return ONLY valid JSON.
"""

    plan = llm.generate_json(
        system_prompt=PLANNER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    if not plan:
        plan = {
            "complexity": "MEDIUM",
            "research_objective": query,
            "keywords": [query],
            "max_sources": 5,
            "report_sections": [
                "Introduction",
                "Main Discussion",
                "Conclusion",
            ],
        }

    state["planner"] = plan

    return state