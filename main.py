"""
AutoResearchAI

Application Entry Point

Runs the complete LangGraph workflow,
stores research memory,
and displays the final report.
"""

from __future__ import annotations

import logging
import time

from graph.workflow import workflow
from memory.chroma import memory

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main() -> None:
    """
    Run the complete research workflow.
    """

    print("=" * 80)
    print("🤖 AutoResearchAI")
    print("Multi-Agent Research System")
    print("=" * 80)

    query = input("\nEnter your research topic:\n> ").strip()

    if not query:
        print("\n❌ Research topic cannot be empty.")
        return

    # -----------------------------------------------------
    # Initial LangGraph State
    # -----------------------------------------------------

    state = {
        "query": query,

        "planner": {},

        "research": {
            "sources": [],
            "documents": [],
            "total_sources": 0,
        },

        "writer": {
            "report": "",
        },

        "review": {
            "score": 0,
            "approved": False,
            "feedback": "",
        },

        "iteration": 0,

        "runtime": 0.0,
    }

    print("\n🚀 Starting research pipeline...\n")

    start_time = time.perf_counter()

    final_state = workflow.invoke(state)

    end_time = time.perf_counter()

    final_state["runtime"] = round(
        end_time - start_time,
        2,
    )

    # -----------------------------------------------------
    # Store Documents in ChromaDB
    # -----------------------------------------------------

    documents = (
        final_state
        .get("research", {})
        .get("documents", [])
    )

    if documents:

        memory.store_documents(
            query=query,
            documents=documents,
        )

    # -----------------------------------------------------
    # Extract Final Results
    # -----------------------------------------------------

    report = (
        final_state
        .get("writer", {})
        .get("report", "No report generated.")
    )

    review = final_state.get("review", {})

    runtime = final_state.get("runtime", 0)

    source_count = (
        final_state
        .get("research", {})
        .get("total_sources", 0)
    )

    # -----------------------------------------------------
    # Console Output
    # -----------------------------------------------------

    print("\n")
    print("=" * 80)
    print("📄 FINAL REPORT")
    print("=" * 80)

    print(report)

    print("\n")
    print("=" * 80)
    print("📝 REVIEW")
    print("=" * 80)

    print(f"⭐ Score       : {review.get('score', 0)}")
    print(f"✅ Approved   : {review.get('approved', False)}")
    print(f"🌐 Sources    : {source_count}")
    print(f"⚡ Runtime    : {runtime} sec")

    print("\nReviewer Feedback:\n")

    print(
        review.get(
            "feedback",
            "No feedback available.",
        )
    )

    print("\n")
    print("=" * 80)
    print(
        f"🧠 Memory Database : {memory.count()} stored documents"
    )
    print("=" * 80)


# ---------------------------------------------------------
# Entry
# ---------------------------------------------------------

if __name__ == "__main__":
    main()