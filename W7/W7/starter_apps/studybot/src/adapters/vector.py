"""Vector store adapters. Pick via VECTOR_BACKEND env var.

Interface:
    ingest(doc_id, text, metadata=None) -> None
    search(query, top_k=5, filter=None) -> list[dict] (each has 'text', 'doc_id', 'score', 'metadata')
"""
import re
from collections import Counter
from typing import Optional


class BedrockKBVector:
    """Production: Bedrock Knowledge Base abstracts the vector store backend.

    Group still chooses the underlying vector store (OpenSearch Serverless, S3 Vectors,
    Aurora pgvector, Pinecone) when creating the KB in AWS console — that choice
    is invisible to this code.

    NOTE: KB ingestion is async via StartIngestionJob, normally triggered by S3 events.
    For simplicity, this adapter is search-only — ingestion happens through the
    Bedrock console or S3 → KB sync pipeline you set up separately.
    """

    def __init__(self, kb_id: str, region: str):
        import boto3
        if not kb_id:
            raise ValueError("VECTOR_BEDROCK_KB_ID must be set for Bedrock KB backend")
        self.kb_id = kb_id
        self.agent_runtime = boto3.client("bedrock-agent-runtime", region_name=region)
        self.agent_client = boto3.client("bedrock-agent", region_name=region)

    def ingest(self, doc_id: str, text: str, metadata: Optional[dict] = None) -> None:
        # Trigger sync of data sources for this Knowledge Base
        try:
            resp = self.agent_client.list_data_sources(knowledgeBaseId=self.kb_id)
            ds_summaries = resp.get("dataSourceSummaries", [])
            if ds_summaries:
                ds_id = ds_summaries[0]["dataSourceId"]
                self.agent_client.start_ingestion_job(
                    knowledgeBaseId=self.kb_id,
                    dataSourceId=ds_id
                )
        except Exception as e:
            import logging
            logging.getLogger("studybot").warning(f"Could not trigger Bedrock KB sync: {e}")

    def search(self, query: str, top_k: int = 5, filter: Optional[dict] = None) -> list:
        # Request a larger pool of results from the API to allow for in-memory filtering
        api_top_k = top_k * 3 if filter else top_k
        kwargs = {
            "knowledgeBaseId": self.kb_id,
            "retrievalQuery": {"text": query},
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {"numberOfResults": api_top_k}
            },
        }
        
        # We do NOT pass the filter to the Bedrock agent_runtime API to avoid ValidationException
        # when metadata fields (like user_id) are not indexed/defined in S3 Vectors.
        resp = self.agent_runtime.retrieve(**kwargs)
        
        results = []
        for r in resp.get("retrievalResults", []):
            content_text = r.get("content", {}).get("text", "")
            score = r.get("score", 0.0)
            
            # Extract metadata from S3 URI
            uri = r.get("location", {}).get("s3Location", {}).get("uri", "")
            extracted_user_id = ""
            extracted_doc_id = ""
            if uri.startswith("s3://"):
                parts = uri[5:].split("/", 2)
                if len(parts) >= 2:
                    extracted_user_id = parts[1]
                    if len(parts) >= 3 and "/" in parts[2]:
                        extracted_doc_id = parts[2].split("/", 1)[0]
            
            metadata = {
                "user_id": extracted_user_id,
                "doc_id": extracted_doc_id,
                "s3_uri": uri
            }
            
            results.append({
                "text": content_text,
                "doc_id": extracted_doc_id,
                "score": score,
                "metadata": metadata,
            })
            
        # Perform in-memory filtering
        if filter:
            filtered_results = []
            for item in results:
                match = True
                for k, v in filter.items():
                    if k == "user_id" and item["metadata"].get("user_id") != v:
                        match = False
                    elif k == "doc_id" and item["doc_id"] != v:
                        match = False
                if match:
                    filtered_results.append(item)
            return filtered_results[:top_k]
            
        return results[:top_k]


class LocalVector:
    """Simple in-memory inverted index + TF scoring. NOT semantic — keyword only.

    Good enough for verifying the API contract locally. Production needs real
    embeddings + ANN — that's what Bedrock KB provides.
    """

    def __init__(self):
        self.docs: list[tuple[str, str, dict]] = []   # (doc_id, text, metadata)

    @staticmethod
    def _tokens(text: str) -> list:
        return [t.lower() for t in re.findall(r"\w+", text) if len(t) > 2]

    @staticmethod
    def _chunk(text: str, size: int = 500) -> list:
        # Naive chunking by sentence-ish boundaries
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks, current = [], ""
        for s in sentences:
            if len(current) + len(s) < size:
                current += " " + s
            else:
                if current.strip():
                    chunks.append(current.strip())
                current = s
        if current.strip():
            chunks.append(current.strip())
        return chunks or [text]

    def ingest(self, doc_id: str, text: str, metadata: Optional[dict] = None) -> None:
        md = metadata or {}
        for i, chunk in enumerate(self._chunk(text)):
            self.docs.append((f"{doc_id}#{i}", chunk, {**md, "doc_id": doc_id, "chunk_idx": i}))

    def search(self, query: str, top_k: int = 5, filter: Optional[dict] = None) -> list:
        q_tokens = set(self._tokens(query))
        results = []
        for chunk_id, text, md in self.docs:
            if filter and not all(md.get(k) == v for k, v in filter.items()):
                continue
            d_tokens = Counter(self._tokens(text))
            score = sum(d_tokens[t] for t in q_tokens)
            if score > 0:
                results.append({
                    "text": text,
                    "doc_id": md.get("doc_id", chunk_id),
                    "score": float(score),
                    "metadata": md,
                })
        results.sort(key=lambda r: -r["score"])
        return results[:top_k]

    def get_user_chunks(self, user_id: str, doc_id: str | None = None, limit: int = 20) -> list:
        """Return chunks for a user (used when keyword search misses broad queries)."""
        results = []
        for _chunk_id, text, md in self.docs:
            if md.get("user_id") != user_id:
                continue
            if doc_id and md.get("doc_id") != doc_id:
                continue
            results.append({
                "text": text,
                "doc_id": md.get("doc_id", ""),
                "score": 1.0,
                "metadata": md,
            })
        return results[:limit]
