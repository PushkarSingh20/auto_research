"""
Planner Agent

Analyzes the user's query and creates a structured research plan.
"""

from __future__ import annotations

import logging

from graph.state import ResearchState
from models.planner import ResearchPlan
from prompts.planner_prompt import PLANNER_SYSTEM_PROMPT
from tools.llm import llm

logger = logging.getLogger(__name__)


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

    logger.info("Planner Agent started.")

    user_prompt = f"""
User Query:

{query}

Return ONLY valid JSON.
"""

    plan = llm.generate_json(
        system_prompt=PLANNER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    if plan:
        try:
            plan = ResearchPlan.model_validate(plan).model_dump()
        except ValueError:
            plan = {}

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

    logger.info("Planner Agent completed.")

    return state
