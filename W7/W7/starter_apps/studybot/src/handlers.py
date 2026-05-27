"""Endpoint handlers. Pure business logic — knows nothing about FastAPI or AWS specifics."""
import io
import json
import re
import uuid
from typing import Any, Optional


PROMPT_TEMPLATE = """You are a study assistant. Answer the student's question using ONLY the
context retrieved from their uploaded lecture notes. Cite the source by chunk
number where possible. If the context does not contain the answer, say so
plainly. Do not invent information.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


def _extract_text(filename: str, data: bytes) -> str:
    """Extract plain text from PDF or .txt upload."""
    name = filename.lower()
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
        except ImportError:
            return "(pypdf not installed — install requirements.txt)"
        reader = PdfReader(io.BytesIO(data))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    # Default: assume UTF-8 text
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def handle_upload(
    user_id: str,
    filename: str,
    data: bytes,
    storage,
    userstore,
    vector_store,
) -> dict:
    """Store the file, extract text, ingest into vector store, record in userstore."""
    doc_id = str(uuid.uuid4())
    key = f"{user_id}/{doc_id}/{filename}"
    location = storage.put(key, data)
    text = _extract_text(filename, data)
    if text.strip():
        vector_store.ingest(doc_id=doc_id, text=text, metadata={"user_id": user_id, "filename": filename})
    userstore.add_doc(
        user_id=user_id,
        doc_id=doc_id,
        metadata={"filename": filename, "size": len(data), "location": location, "chars": len(text)},
    )
    return {
        "doc_id": doc_id,
        "filename": filename,
        "size": len(data),
        "chars_extracted": len(text),
        "location": location,
    }


def handle_query(
    user_id: str,
    question: str,
    ai_client,
    userstore,
    vector_store,
    vector_backend: str,
    bedrock_kb_id: str,
) -> dict:
    """RAG flow: retrieve user's relevant chunks → call AI with context → log + return."""
    if vector_backend == "bedrock_kb":
        # Production path: let Bedrock do retrieve + generate in one call
        result = ai_client.retrieve_and_generate(query=question, kb_id=bedrock_kb_id)
        answer = result["answer"]
        citations = result["citations"]
    else:
        # Local path: do our own retrieve then prompt
        chunks = vector_store.search(question, top_k=5, filter={"user_id": user_id})
        if not chunks:
            answer = "No relevant content found in your uploaded documents. Upload some first."
            citations = []
        else:
            context = "\n\n".join(f"[chunk {i+1}] {c['text']}" for i, c in enumerate(chunks))
            prompt = PROMPT_TEMPLATE.format(context=context, question=question)
            answer = ai_client.invoke(prompt, max_tokens=512)
            citations = [
                {"chunk": i + 1, "doc_id": c["doc_id"], "score": c["score"], "text": c["text"][:200]}
                for i, c in enumerate(chunks)
            ]

    userstore.log_query(user_id=user_id, query=question, answer=answer)
    return {"question": question, "answer": answer, "citations": citations}


def handle_list_docs(user_id: str, userstore) -> dict:
    return {"user_id": user_id, "docs": userstore.list_docs(user_id)}


def handle_recent_queries(user_id: str, userstore, limit: int = 10) -> dict:
    return {"user_id": user_id, "queries": userstore.recent_queries(user_id, limit=limit)}


# ---- Study tools: summary / flashcards / quiz ----

_EMPTY_DOCS_MSG = (
    "No relevant content found in your uploaded documents. Upload a PDF or TXT first."
)


def _parse_json_from_llm(text: str) -> Any:
    """Extract JSON from model output (raw JSON or fenced code block)."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fenced:
        try:
            return json.loads(fenced.group(1).strip())
        except json.JSONDecodeError:
            pass
    brace = re.search(r"\{[\s\S]*\}|\[[\s\S]*\]", text)
    if brace:
        return json.loads(brace.group(0))
    raise ValueError("Model did not return valid JSON")


def _gather_context(
    user_id: str,
    vector_store,
    doc_id: Optional[str] = None,
    top_k: int = 15,
) -> list[dict]:
    """Retrieve chunks from the user's documents for study-tool generation."""
    broad_query = "summary overview main topics key concepts definitions lecture"
    chunks = vector_store.search(broad_query, top_k=top_k * 2, filter={"user_id": user_id})
    if doc_id:
        chunks = [c for c in chunks if c.get("doc_id") == doc_id]
    if len(chunks) < 3 and hasattr(vector_store, "get_user_chunks"):
        chunks = vector_store.get_user_chunks(user_id, doc_id=doc_id, limit=top_k)
    return chunks[:top_k]


def _context_block(chunks: list[dict]) -> str:
    return "\n\n".join(f"[chunk {i + 1}] {c['text']}" for i, c in enumerate(chunks))


def _citations_from_chunks(chunks: list[dict]) -> list[dict]:
    return [
        {"chunk": i + 1, "doc_id": c["doc_id"], "score": c["score"], "text": c["text"][:200]}
        for i, c in enumerate(chunks)
    ]


SUMMARY_PROMPT = """You are a study assistant. Using ONLY the lecture context below, produce a JSON object:
{{
  "summary": "2-4 paragraph study guide suitable for exam prep",
  "key_concepts": ["exactly 5 most testable concepts as short phrases"]
}}

Rules: base everything on the context; do not invent facts; respond with ONLY valid JSON.

CONTEXT:
{context}
"""

FLASHCARDS_PROMPT = """You are a study assistant. Using ONLY the lecture context below, produce a JSON object:
{{
  "flashcards": [
    {{"front": "question or term", "back": "concise answer or definition"}},
    ... exactly {count} items
  ]
}}

Rules: varied difficulty; each card tests one idea from the context; respond with ONLY valid JSON.

CONTEXT:
{context}
"""

QUIZ_PROMPT = """You are a study assistant. Using ONLY the lecture context below, produce a JSON object:
{{
  "questions": [
    {{
      "question": "clear multiple-choice stem",
      "options": ["option A", "option B", "option C", "option D"],
      "correct_index": 0,
      "explanation": "why the correct answer is right, citing the material"
    }},
    ... exactly {count} items
  ]
}}

Rules: one clearly correct answer per question; plausible distractors; correct_index is 0-3; respond with ONLY valid JSON.

CONTEXT:
{context}
"""


def handle_summary(
    user_id: str,
    ai_client,
    vector_store,
    doc_id: Optional[str] = None,
) -> dict:
    chunks = _gather_context(user_id, vector_store, doc_id=doc_id)
    if not chunks:
        return {"summary": _EMPTY_DOCS_MSG, "key_concepts": [], "citations": []}
    prompt = SUMMARY_PROMPT.format(context=_context_block(chunks))
    raw = ai_client.invoke(prompt, max_tokens=1536)
    try:
        data = _parse_json_from_llm(raw)
    except (ValueError, json.JSONDecodeError):
        data = {"summary": raw.strip(), "key_concepts": []}
    return {
        "doc_id": doc_id,
        "summary": data.get("summary", ""),
        "key_concepts": data.get("key_concepts", [])[:5],
        "citations": _citations_from_chunks(chunks),
    }


def handle_flashcards(
    user_id: str,
    ai_client,
    vector_store,
    doc_id: Optional[str] = None,
    count: int = 10,
) -> dict:
    count = max(1, min(count, 20))
    chunks = _gather_context(user_id, vector_store, doc_id=doc_id)
    if not chunks:
        return {"doc_id": doc_id, "flashcards": [], "citations": []}
    prompt = FLASHCARDS_PROMPT.format(context=_context_block(chunks), count=count)
    raw = ai_client.invoke(prompt, max_tokens=2048)
    try:
        data = _parse_json_from_llm(raw)
        cards = data.get("flashcards", [])
    except (ValueError, json.JSONDecodeError):
        cards = []
    normalized = [
        {"front": str(c.get("front", "")), "back": str(c.get("back", ""))}
        for c in cards
        if isinstance(c, dict) and (c.get("front") or c.get("back"))
    ][:count]
    return {
        "doc_id": doc_id,
        "flashcards": normalized,
        "citations": _citations_from_chunks(chunks),
    }


def handle_quiz(
    user_id: str,
    ai_client,
    vector_store,
    doc_id: Optional[str] = None,
    count: int = 10,
) -> dict:
    count = max(1, min(count, 20))
    chunks = _gather_context(user_id, vector_store, doc_id=doc_id)
    if not chunks:
        return {"doc_id": doc_id, "questions": [], "citations": []}
    prompt = QUIZ_PROMPT.format(context=_context_block(chunks), count=count)
    raw = ai_client.invoke(prompt, max_tokens=3072)
    try:
        data = _parse_json_from_llm(raw)
        questions = data.get("questions", [])
    except (ValueError, json.JSONDecodeError):
        questions = []
    normalized = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        opts = q.get("options") or []
        if len(opts) < 2:
            continue
        idx = int(q.get("correct_index", 0))
        idx = max(0, min(idx, len(opts) - 1))
        normalized.append({
            "question": str(q.get("question", "")),
            "options": [str(o) for o in opts[:4]],
            "correct_index": idx,
            "explanation": str(q.get("explanation", "")),
        })
    return {
        "doc_id": doc_id,
        "questions": normalized[:count],
        "citations": _citations_from_chunks(chunks),
    }
