"""AI adapters. Pick via AI_BACKEND env var.

Interface:
    invoke(prompt, **kwargs) -> str
    retrieve_and_generate(query, kb_id="") -> dict with {"answer": str, "citations": list}
"""
import json
import re
from typing import Any


class BedrockAI:
    """Real Amazon Bedrock client. Uses Converse API for invoke; bedrock-agent-runtime for RAG."""

    def __init__(self, region: str, model_id: str):
        import boto3
        self.region = region
        self.model_id = model_id
        self.runtime = boto3.client("bedrock-runtime", region_name=region)
        self.agent_runtime = boto3.client("bedrock-agent-runtime", region_name=region)

    def invoke(self, prompt: str, **kwargs: Any) -> str:
        max_tokens = kwargs.get("max_tokens", 1024)
        resp = self.runtime.converse(
            modelId=self.model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": max_tokens, "temperature": kwargs.get("temperature", 0.2)},
        )
        return resp["output"]["message"]["content"][0]["text"]

    def retrieve_and_generate(self, query: str, kb_id: str = "") -> dict:
        if not kb_id:
            raise ValueError("VECTOR_BEDROCK_KB_ID must be set for Bedrock KB retrieve_and_generate")
        model_arn = f"arn:aws:bedrock:{self.region}::foundation-model/{self.model_id}"
        resp = self.agent_runtime.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": kb_id,
                    "modelArn": model_arn,
                },
            },
        )
        return {
            "answer": resp["output"]["text"],
            "citations": [
                {
                    "text": ref.get("content", {}).get("text", ""),
                    "source": ref.get("location", {}),
                }
                for citation in resp.get("citations", [])
                for ref in citation.get("retrievedReferences", [])
            ],
        }


def _first_chunk_snippet(prompt: str, max_len: int = 280) -> str:
    m = re.search(r"\[chunk 1\]\s*(.+?)(?:\n\n\[chunk|\Z)", prompt, re.DOTALL)
    text = (m.group(1) if m else prompt).strip()
    return text[:max_len]


class LocalAI:
    """Local stub. Returns canned responses. Use for development without AWS credentials."""

    def invoke(self, prompt: str, **kwargs: Any) -> str:
        snippet = _first_chunk_snippet(prompt)
        if '"key_concepts"' in prompt or "study guide" in prompt.lower():
            return json.dumps({
                "summary": (
                    f"[LOCAL_AI_STUB] Study guide from your notes:\n\n{snippet}\n\n"
                    "Set AI_BACKEND=bedrock for a full AI-generated summary."
                ),
                "key_concepts": [
                    "Core idea from uploaded material",
                    "Supporting definition or process",
                    "Cause and effect relationship",
                    "Comparison or contrast point",
                    "Application or example",
                ],
            })
        if '"flashcards"' in prompt:
            count_m = re.search(r"exactly (\d+) items", prompt)
            n = int(count_m.group(1)) if count_m else 5
            cards = [
                {"front": f"Key term {i + 1}?", "back": f"Answer drawn from: {snippet[:80]}…"}
                for i in range(min(n, 5))
            ]
            return json.dumps({"flashcards": cards})
        if '"questions"' in prompt and '"correct_index"' in prompt:
            count_m = re.search(r"exactly (\d+) items", prompt)
            n = int(count_m.group(1)) if count_m else 5
            questions = []
            for i in range(min(n, 3)):
                questions.append({
                    "question": f"According to your notes, which statement is correct? (Q{i + 1})",
                    "options": [
                        "A fact supported by the uploaded content",
                        "An unrelated distractor",
                        "Another plausible but wrong option",
                        "A third distractor",
                    ],
                    "correct_index": 0,
                    "explanation": f"Based on chunk content: {snippet[:100]}…",
                })
            return json.dumps({"questions": questions})
        short = prompt[:200].replace("\n", " ")
        return (
            f"[LOCAL_AI_STUB] Received prompt: {short!r}... "
            "Set AI_BACKEND=bedrock + AWS credentials for real Bedrock output."
        )

    def retrieve_and_generate(self, query: str, kb_id: str = "") -> dict:
        return {
            "answer": (
                f"[LOCAL_AI_STUB] Query received: {query!r}. "
                "Set AI_BACKEND=bedrock and VECTOR_BACKEND=bedrock_kb for real RAG."
            ),
            "citations": [],
        }
