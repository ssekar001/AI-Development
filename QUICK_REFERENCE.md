# Quick Reference Guide

## Common Operations

### Initialize the System

```python
from mongo_model import MongoVectorDB
from ai import AzureOpenAIVectorModel

# Connect to MongoDB
mongo_db = MongoVectorDB()

# Initialize Azure OpenAI
ai_model = AzureOpenAIVectorModel()
```

### Store Documents with Embeddings

```python
# Single document
text = "Your document text here"
embedding = ai_model.create_embedding(text)
doc_id = mongo_db.insert_document(
    text=text, 
    embedding=embedding,
    metadata={"source": "example", "category": "demo"}
)

# Multiple documents
texts = ["Doc 1", "Doc 2", "Doc 3"]
embeddings = ai_model.create_embeddings_batch(texts)

docs = [
    {"text": t, "embedding": e, "metadata": {"index": i}}
    for i, (t, e) in enumerate(zip(texts, embeddings))
]
ids = mongo_db.batch_insert_documents(docs)
```

### Search and Query

```python
# Create query embedding
query = "What is X?"
query_embedding = ai_model.create_embedding(query)

# Find similar documents
results = mongo_db.search_by_similarity(query_embedding, limit=5)

# Generate response using RAG
response = ai_model.generate_response(query, results)
print(response)
```

### Streaming Responses

```python
query = "Your question"
docs = mongo_db.search_by_similarity(
    ai_model.create_embedding(query), 
    limit=3
)

print("Response: ", end="", flush=True)
for chunk in ai_model.generate_streaming_response(query, docs):
    print(chunk, end="", flush=True)
print()
```

### Document Management

```python
# Get specific document
doc = mongo_db.get_document_by_id(doc_id)

# Get all documents
all_docs = mongo_db.get_all_documents(limit=100)

# Delete document
success = mongo_db.delete_document(doc_id)

# Clear all
mongo_db.clear_collection()
```

### Context Manager Pattern

```python
# Automatically closes connection
with MongoVectorDB() as mongo_db:
    with AzureOpenAIVectorModel() as ai_model:
        # Your code here
        pass
    # Connection automatically closed
```

## Configuration

### Create .env File

```bash
# Copy template
cp .env.template .env

# Edit with your values
MONGO_CONNECTION_STRING=mongodb+srv://...
AZURE_OPENAI_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
```

### Load Environment Variables in Python

```python
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

# Access variables
mongo_connection = os.getenv("MONGO_CONNECTION_STRING")
openai_key = os.getenv("AZURE_OPENAI_KEY")
```

## Error Handling

### Handle Connection Errors

```python
try:
    mongo_db = MongoVectorDB()
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    # Handle error

try:
    ai_model = AzureOpenAIVectorModel()
except Exception as e:
    print(f"Failed to initialize Azure OpenAI: {e}")
    # Handle error
```

### Handle API Errors

```python
try:
    embedding = ai_model.create_embedding("text")
except Exception as e:
    print(f"Embedding creation failed: {e}")

try:
    response = ai_model.generate_response(query, docs)
except Exception as e:
    print(f"Response generation failed: {e}")
```

## Sample Data

### Use Pre-built Samples

```python
ai_model = AzureOpenAIVectorModel()
samples = ai_model.prepare_sample_data()

# samples contains:
# [{text: "...", metadata: {...}}, ...]
```

### Setup Complete Pipeline

```python
from ai import setup_rag_pipeline

success = setup_rag_pipeline(mongo_db, ai_model)
```

## Custom System Prompts

```python
custom_prompt = """You are an expert in machine learning.
Answer questions based on the provided documents.
Be concise and technical."""

response = ai_model.generate_response(
    query=query,
    context_documents=docs,
    system_prompt=custom_prompt
)
```

## Batch Processing

### Process Large Datasets

```python
# Batch embedding creation
batch_size = 100
all_texts = [...]  # Your texts

for i in range(0, len(all_texts), batch_size):
    batch = all_texts[i:i+batch_size]
    embeddings = ai_model.create_embeddings_batch(batch)
    
    docs = [
        {"text": t, "embedding": e, "metadata": {...}}
        for t, e in zip(batch, embeddings)
    ]
    mongo_db.batch_insert_documents(docs)
```

## Performance Tips

```python
# Good: Batch operations
embeddings = ai_model.create_embeddings_batch(texts)  # ✓ Fast
ids = mongo_db.batch_insert_documents(docs)           # ✓ Fast

# Avoid: One at a time
for text in texts:
    embedding = ai_model.create_embedding(text)       # ✗ Slow
    mongo_db.insert_document(text, embedding)         # ✗ Slow

# Good: Limit results
results = mongo_db.search_by_similarity(emb, limit=10)  # ✓ Fast

# Avoid: No limit
results = mongo_db.get_all_documents()                   # ✗ Slow
```

## Logging

### Add Simple Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting RAG pipeline")
try:
    response = ai_model.generate_response(query, docs)
    logger.info(f"Generated response: {response[:100]}...")
except Exception as e:
    logger.error(f"Error generating response: {e}")
```

## Testing

### Quick Test

```python
# Run the full demo
python test.py

# Test individual components
from mongo_model import MongoVectorDB
db = MongoVectorDB()
print("MongoDB connected!")

from ai import AzureOpenAIVectorModel
ai = AzureOpenAIVectorModel()
print("Azure OpenAI connected!")
```

### Unit Test Template

```python
import unittest
from mongo_model import MongoVectorDB
from ai import AzureOpenAIVectorModel

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.mongo_db = MongoVectorDB()
        self.ai_model = AzureOpenAIVectorModel()
    
    def test_embedding_creation(self):
        embedding = self.ai_model.create_embedding("test")
        self.assertIsNotNone(embedding)
        self.assertEqual(len(embedding), 1536)
    
    def test_document_insertion(self):
        embedding = self.ai_model.create_embedding("test")
        doc_id = self.mongo_db.insert_document(
            "test", embedding, {}
        )
        self.assertIsNotNone(doc_id)
    
    def tearDown(self):
        self.mongo_db.close()

if __name__ == '__main__':
    unittest.main()
```

## Debugging

### Check Configuration

```python
import os

print("MongoDB Connection:", os.getenv("MONGO_CONNECTION_STRING")[:20] + "...")
print("Azure OpenAI Key:", os.getenv("AZURE_OPENAI_KEY")[:10] + "...")
print("Azure OpenAI Endpoint:", os.getenv("AZURE_OPENAI_ENDPOINT"))
```

### Test Connections

```python
from mongo_model import MongoVectorDB
from ai import AzureOpenAIVectorModel

# Test MongoDB
try:
    db = MongoVectorDB()
    print("✓ MongoDB connected")
    db.close()
except Exception as e:
    print(f"✗ MongoDB error: {e}")

# Test Azure OpenAI
try:
    ai = AzureOpenAIVectorModel()
    embedding = ai.create_embedding("test")
    print(f"✓ Azure OpenAI working (embedding: {len(embedding)} dims)")
except Exception as e:
    print(f"✗ Azure OpenAI error: {e}")
```

### Monitor API Usage

```python
import time

start = time.time()
embedding = ai_model.create_embedding("test")
duration = time.time() - start
print(f"Embedding took {duration:.2f}s")

start = time.time()
response = ai_model.generate_response(query, docs)
duration = time.time() - start
print(f"Response took {duration:.2f}s")
```

## Common Issues & Solutions

### "No module named 'pymongo'"
```bash
pip install pymongo
```

### "MONGO_CONNECTION_STRING not found"
```bash
# Create .env file or set environment variable
export MONGO_CONNECTION_STRING="mongodb+srv://..."
```

### "Authentication failed for Azure OpenAI"
```bash
# Check credentials
echo $AZURE_OPENAI_KEY
echo $AZURE_OPENAI_ENDPOINT

# Run az login if using CLI credentials
az login
```

### MongoDB Connection Timeout
```python
# Increase timeout
from pymongo import MongoClient
client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
```

## Useful Commands

```bash
# Install all dependencies
pip install -r requirements.txt

# Run main demo
python test.py

# Run with specific env file
export $(cat .env | xargs) && python test.py

# Check Python version
python --version

# List installed packages
pip list

# Update package
pip install --upgrade pymongo openai

# Create new virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Next Steps

1. Update `.env` with your credentials
2. Run `python test.py` to verify setup
3. Customize `prepare_sample_data()` with your data
4. Build your application on top of this foundation
5. Deploy to production with security best practices

Happy coding! 🚀
