"""
Centralized logging configuration for AutoResearchAI.
"""

from __future__ import annotations

import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "autoresearch.log"


def setup_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger.

    Every module should obtain its logger through this function.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File output
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger