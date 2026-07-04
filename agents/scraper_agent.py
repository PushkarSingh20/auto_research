"""
Scraper Agent

Downloads and cleans the content of
all sources collected by the Research Agent.
"""

from __future__ import annotations

import logging

from graph.state import ResearchState
from tools.scraper import scrape_url

logger = logging.getLogger(__name__)


def scraper_node(state: ResearchState) -> ResearchState:
    """
    Scrape all research sources.

    Args:
        state: Current LangGraph state.

    Returns:
        Updated state containing cleaned documents.
    """

    logger.info("Scraper Agent started.")

    sources = state.get("research", {}).get("sources", [])

    documents = []

    for source in sources:

        content = scrape_url(source["url"])

        if not content:
            continue

        documents.append(
            {
                "title": source["title"],
                "url": source["url"],
                "snippet": source["snippet"],
                "content": content,
                "source_type": "web",
                "content_length": len(content),
            }
        )

    state.setdefault("research", {})
    state["research"]["documents"] = documents

    logger.info(
        "Scraper Agent collected %d documents.",
        len(documents),
    )

    return state