import boto3

try:
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1"
    )
    
    resp = client.converse(
        modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        messages=[{"role": "user", "content": [{"text": "Hello, how are you?"}]}],
        inferenceConfig={"maxTokens": 10}
    )
    print("SUCCESS!")
    print(resp["output"]["message"]["content"][0]["text"])
except Exception as e:
    import traceback
    print("FAILED!")
    traceback.print_exc()
