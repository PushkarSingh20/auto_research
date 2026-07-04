"""
Web Scraper Tool

Downloads webpages and extracts clean textual content.
"""

from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def scrape_url(
    url: str,
    timeout: int = 10,
    max_chars: int = 5000,
) -> str:
    """
    Download a webpage and return cleaned text.

    Args:
        url: Target webpage.
        timeout: Request timeout.
        max_chars: Maximum characters returned.

    Returns:
        Clean extracted text.
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=timeout,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "footer",
                "header",
                "nav",
                "form",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True,
        )

        text = " ".join(text.split())

        logger.info("Scraped %s", url)

        return text[:max_chars]

    except Exception:

        logger.exception("Failed to scrape %s", url)

        return ""