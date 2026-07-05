"""
Writer Agent

Generates the first draft of the research report
using the scraped documents.
"""

from __future__ import annotations

import logging

from graph.state import ResearchState
from prompts.writer_prompt import (
    WRITER_SYSTEM_PROMPT,
    build_writer_prompt,
)
from tools.llm import llm

logger = logging.getLogger(__name__)


def writer_node(state: ResearchState) -> ResearchState:
    """
    Generate a research report.

    Args:
        state: Current LangGraph state.

    Returns:
        Updated state containing the generated report.
    """

    logger.info("Writer Agent started.")

    query = state["query"]

    documents = state.get("research", {}).get("documents", [])
    review = state.get("review", {})
    previous_report = state.get("writer", {}).get("report", "")
    iteration = state.get("iteration", 0)

    if not documents:
        logger.warning("No documents available.")
        report = "# Report\n\nNo research documents were found."
    else:
        context = "\n\n".join(

            f"""
TITLE:
{doc["title"]}

SOURCE:
{doc["url"]}

CONTENT:
{doc["content"]}
"""

            for doc in documents

        )

        prompt = build_writer_prompt(
            query=query,
            context=context,
            previous_report=previous_report,
            reviewer_feedback=review.get("feedback", ""),
            weaknesses=review.get("weaknesses", []),
            iteration=iteration,
        )

        report = llm.generate_text(

            system_prompt=WRITER_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.3,
            max_tokens=2500,

        )

        if not report.strip():

            logger.warning("Writer returned an empty report.")

            report = "# Report\n\nUnable to generate report."

    state.setdefault("writer", {})
    state["writer"]["report"] = report
    state["iteration"] = iteration + 1

    logger.info("Writer Agent completed.")

    return state
