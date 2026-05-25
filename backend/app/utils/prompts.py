from typing import Any

from app.config import CV_HISTORY_MAX_CHARS, CV_HISTORY_MAX_TURNS


def build_question_rewrite_prompt(
    question: str,
    history: list[dict[str, str]],
) -> str:
    conversation = build_conversation_context(history)
    return f"""You are a search query rewriting assistant for a CV screening system.

Rewrite the user's latest question into a standalone question that captures the conversation history and the current question.
Use the conversation history only to resolve follow-up questions, pronouns, and omitted details.
Return only the rewritten question. Do not add quotes, bullets, or explanations.

Conversation history:
{conversation}

Latest user question:
{question}

Rewritten question:"""


def build_prompt(question: str, cvs: list[dict[str, Any]]) -> str:
    context = build_cv_context(cvs)
    return f"""You are an AI CV screening assistant.

Answer the user's question using only the retrieved CV context below.
Do not use outside knowledge.
If the answer cannot be found in the context, say that the information is not available in the indexed CVs.
When possible, mention the candidate name and source PDF filename.
Do not mention embeddings, vector search, or query rewriting.

Question:
{question}

Retrieved CV context:
{context}

Answer:"""


def build_cv_context(
    cvs: list[dict[str, Any]],
) -> str:
    context_blocks = []
    for index, cv in enumerate(cvs, start=1):
        metadata = cv["metadata"]
        context_blocks.append(
            "\n".join(
                [
                    f"Source {index}",
                    f"Candidate: {metadata.get('candidate_name', 'unknown')}",
                    f"File: {metadata.get('filename', 'unknown')}",
                    f"Page: {metadata.get('page_number', 'unknown')}",
                    "Text:",
                    cv["text"],
                ]
            )
        )
    return "\n\n---\n\n".join(context_blocks)


def build_conversation_context(history: list[dict[str, str]]) -> str:
    recent_history = history[-CV_HISTORY_MAX_TURNS:]
    formatted_turns = []

    for turn in recent_history:
        role = turn.get("role", "unknown")
        content = turn.get("content", "").strip()
        if content:
            formatted_turns.append(f"{role.title()}: {content}")

    context = "\n".join(formatted_turns).strip()
    if len(context) > CV_HISTORY_MAX_CHARS:
        context = context[-CV_HISTORY_MAX_CHARS:].lstrip()

    return context or "No prior conversation."
