"""
Reviewer Agent

Evaluates the generated research report and
provides structured feedback.
"""

from __future__ import annotations

import logging

from graph.state import ResearchState
from prompts.reviewer_prompt import (
    REVIEWER_SYSTEM_PROMPT,
    build_reviewer_prompt,
)
from tools.llm import llm

logger = logging.getLogger(__name__)


def reviewer_node(state: ResearchState) -> ResearchState:
    """
    Review the generated report.

    Args:
        state: Current LangGraph state.

    Returns:
        Updated ResearchState containing review results.
    """

    logger.info("Reviewer Agent started.")

    report = state.get("writer", {}).get("report", "")

    if not report.strip():

        logger.warning("No report found for review.")

        state["review"] = {
            "score": 0.0,
            "approved": False,
            "strengths": [],
            "weaknesses": [
                "No report available."
            ],
            "feedback": "Generate a report first."
        }

        return state

    prompt = build_reviewer_prompt(report)

    review = llm.generate_json(

        system_prompt=REVIEWER_SYSTEM_PROMPT,
        user_prompt=prompt,

    )

    if not review:

        logger.warning("Reviewer returned invalid JSON.")

        review = {
            "score": 0.0,
            "approved": False,
            "strengths": [],
            "weaknesses": [
                "Unable to evaluate report."
            ],
            "feedback": "Reviewer failed."
        }

    state["review"] = review

    logger.info(
        "Reviewer completed. Score: %s",
        review.get("score", 0),
    )

    return state