import boto3
from typing import Optional

class BedrockKBVector:
    def __init__(self, kb_id: str, region: str):
        self.kb_id = kb_id
        self.agent_runtime = boto3.client(
            "bedrock-agent-runtime",
            region_name=region
        )

    def search(self, query: str, top_k: int = 5, filter: Optional[dict] = None) -> list:
        api_top_k = top_k * 3 if filter else top_k
        kwargs = {
            "knowledgeBaseId": self.kb_id,
            "retrievalQuery": {"text": query},
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {"numberOfResults": api_top_k}
            },
        }
        
        resp = self.agent_runtime.retrieve(**kwargs)
        
        results = []
        for r in resp.get("retrievalResults", []):
            content_text = r.get("content", {}).get("text", "")
            score = r.get("score", 0.0)
            
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

try:
    vector = BedrockKBVector("1IVSEQCTFP", "us-east-1")
    print("Calling search...")
    res = vector.search("photosynthesis", top_k=5, filter={"user_id": "test-user-001"})
    print("SUCCESS! Results found:", len(res))
    for idx, r in enumerate(res):
        print(f"\nResult {idx+1}:")
        print(f"  doc_id: {r['doc_id']}")
        print(f"  user_id: {r['metadata']['user_id']}")
        print(f"  score: {r['score']}")
        print(f"  text snippet: {r['text'][:100]}")
except Exception as e:
    import traceback
    print("FAILED!")
    traceback.print_exc()
