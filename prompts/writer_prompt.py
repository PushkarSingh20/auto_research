"""
Prompt used by the Writer Agent.
"""

WRITER_SYSTEM_PROMPT = """
You are an expert AI research writer.

Your job is to write a professional research report.

Rules:

- Use Markdown formatting.
- Include meaningful headings.
- Explain concepts clearly.
- Do not hallucinate facts.
- Use only the provided context.
- If information is missing, explicitly mention it.
- Write in a formal research style.

Structure:

# Title

## Introduction

## Key Findings

## Analysis

## Conclusion
"""


def build_writer_prompt(
    *,
    query: str,
    context: str,
    previous_report: str = "",
    reviewer_feedback: str = "",
    weaknesses: list[str] | None = None,
    iteration: int = 0,
) -> str:
    """
    Build the user prompt for the Writer Agent.
    """

    revision_context = ""

    if iteration > 0 and previous_report:
        weakness_text = "\n".join(f"- {item}" for item in weaknesses or [])
        revision_context = f"""
Previous Report:

{previous_report}

Reviewer Feedback:

{reviewer_feedback or "No feedback provided."}

Weaknesses To Fix:

{weakness_text or "- No specific weaknesses provided."}

This is revision iteration {iteration}. Improve the previous report
using the feedback above while staying faithful to the research context.
"""

    return f"""
Research Topic:

{query}

Available Research Context:

{context}

{revision_context}

Using ONLY the above context, generate a comprehensive,
well-structured research report in Markdown.

Do not invent information that is not present in the context.
"""
