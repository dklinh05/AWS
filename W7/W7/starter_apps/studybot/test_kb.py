import boto3
import sys

try:
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name="us-east-1"
    )
    
    resp = client.retrieve(
        knowledgeBaseId="1IVSEQCTFP",
        retrievalQuery={"text": "photosynthesis"},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": 5}
        }
    )
    print("SUCCESS!")
    print(resp)
except Exception as e:
    import traceback
    print("FAILED!")
    traceback.print_exc()
