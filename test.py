import os
import sys
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

# Simple Azure OpenAI chat call
# Requires these environment variables to be set:
# - AZURE_OPENAI_ENDPOINT (e.g. https://your-resource.openai.azure.com)
# - AZURE_OPENAI_KEY
# - AZURE_OPENAI_DEPLOYMENT (your chat deployment id, e.g. gpt-35-turbo)

def chat(prompt: str, max_tokens: int = 200) -> str:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not endpoint or not key or not deployment:
        print("Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY and AZURE_OPENAI_DEPLOYMENT environment variables.", file=sys.stderr)
        sys.exit(1)

    client = OpenAIClient(endpoint, AzureKeyCredential(key))

    response = client.get_chat_completions(
        deployment_id=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Example prompt to trigger a response
    prompt = "Say hello in two sentences and mention the day of the week."
    print("Sending prompt:\n", prompt)

    try:
        reply = chat(prompt)
        print("\nModel reply:\n", reply)
    except Exception as exc:
        print("Error calling Azure OpenAI:", exc, file=sys.stderr)
        sys.exit(1)
