import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
from pymongo import MongoClient

mongo_client = MongoClient(
    "mongodb://atlas-sql-6a00b3d451cd206c38a7aff8-jmi4ok.z.query.mongodb.net/vectordb?ssl=true&authSource=admin"
)

db = mongo_client["vectordb"]
collection = db["documents"]
documents = [
    "Azure AI Foundry helps build enterprise AI applications.",
    "MongoDB supports vector similarity search.",
    "Embeddings convert text into numerical vectors.",
    "RAG combines retrieval and generation.",
    "Vector databases improve semantic search."
]
for text in documents:

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    embedding = response.data[0].embedding

    collection.insert_one({
        "text": text,
        "embedding": embedding
    })

print("Embeddings stored successfully")
