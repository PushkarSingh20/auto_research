"""
Shared LangGraph state.

Every node reads and updates this state.
"""

from typing import Any, TypedDict


class ResearchState(TypedDict):
    query: str

    planner: dict[str, Any]

    research: dict[str, Any]

    writer: dict[str, Any]

    review: dict[str, Any]

    iteration: int