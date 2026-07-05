"""
Search Tool

Performs web searches using DuckDuckGo.

This module is responsible ONLY for searching the web.
It does not scrape webpages or generate reports.
"""

from __future__ import annotations

import logging

from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


def search_web(
    keywords: list[str],
    max_results: int = 5,
) -> list[dict]:
    """
    Search the web using DuckDuckGo.

    Args:
        keywords: List of search keywords.
        max_results: Maximum number of search results.

    Returns:
        List of dictionaries containing:
            - title
            - url
            - snippet
    """

    if not keywords:
        logger.warning("No keywords provided for search.")
        return []

    query = " ".join(keywords)

    search_results: list[dict] = []
    seen_urls: set[str] = set()

    try:
        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=max_results,
            )

            for result in results:

                url = result.get("href", "").strip()

                if not url:
                    continue

                if url in seen_urls:
                    continue

                seen_urls.add(url)

                search_results.append(
                    {
                        "title": result.get("title", "Untitled"),
                        "url": url,
                        "snippet": result.get("body", ""),
                    }
                )

        logger.info(
            "Found %d search results for '%s'",
            len(search_results),
            query,
        )

        return search_results

    except Exception as exc:
        logger.warning("Search failed: %s", exc)
        return []
