# Azure OpenAI + MongoDB Vector Database Setup Guide

## Prerequisites

- Azure Subscription with OpenAI Service deployed
- Azure MongoDB instance (Atlas or Azure Cosmos DB for MongoDB)
- Python 3.8+
- pip package manager

## Installation Steps

### 1. Install Dependencies

```bash
# Activate your virtual environment (if using one)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `AI-Development` directory or set environment variables:

#### MongoDB Connection
```bash
export MONGO_CONNECTION_STRING="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
```

#### Azure OpenAI Configuration
```bash
export AZURE_OPENAI_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-05-01-preview"
export AZURE_EMBEDDING_MODEL="text-embedding-3-small"
export AZURE_CHAT_MODEL="gpt-4o-mini"
```

#### Optional: Azure AI Foundry (if using)
```bash
export AZURE_FOUNDRY_PROJECT_ENDPOINT="https://your-resource.services.ai.azure.com/"
export AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME="your-deployment-name"
```

### 3. Get Your Configuration Values

#### MongoDB Connection String
1. Go to Azure Portal or MongoDB Atlas
2. Find your MongoDB instance
3. Click "Connection" or "Get Connection String"
4. Copy the connection string with your credentials
5. Format: `mongodb+srv://username:password@host/?retryWrites=true&w=majority`

#### Azure OpenAI Configuration
1. Go to Azure Portal → OpenAI Service
2. Navigate to "Keys and Endpoint"
3. Copy your API Key and Endpoint URL
4. Go to "Model deployments" and note your deployment names
5. Ensure you have embeddings (text-embedding-3-small) and chat (gpt-4o-mini) models deployed

## Usage

### Basic Usage

```python
from mongo_model import MongoVectorDB
from ai import AzureOpenAIVectorModel, setup_rag_pipeline

# Initialize connections
mongo_db = MongoVectorDB()
ai_model = AzureOpenAIVectorModel()

# Setup with sample data
setup_rag_pipeline(mongo_db, ai_model)

# Create embedding for a query
query = "Your question here"
embedding = ai_model.create_embedding(query)

# Search similar documents
similar_docs = mongo_db.search_by_similarity(embedding)

# Generate response with RAG
response = ai_model.generate_response(query, similar_docs)
print(response)

# Cleanup
mongo_db.close()
```

### Run the Demo

```bash
python test.py
```

This will:
1. Connect to MongoDB
2. Initialize Azure OpenAI
3. Load sample data with embeddings
4. Perform searches and generate responses
5. Display results

## Architecture

```
┌─────────────────────────────────────────┐
│     Azure OpenAI Service                │
│  - Embeddings (text-embedding-3-small)  │
│  - Chat Completion (gpt-4o-mini)        │
└──────────────┬──────────────────────────┘
               │
               │ Embeddings API
               │ Chat Completion API
               │
        ┌──────▼──────────┐
        │   ai.py         │
        │  (RAG Logic)    │
        └──────┬──────────┘
               │
               │ Insert Documents
               │ Search Vectors
               │
        ┌──────▼──────────────┐
        │   MongoDB Atlas     │
        │  (Vector Storage)   │
        └────────────────────┘
```

## Module Documentation

### mongo_model.py - MongoVectorDB

**Methods:**
- `insert_document(text, embedding, metadata)` - Insert single document with embedding
- `batch_insert_documents(documents)` - Insert multiple documents
- `search_by_similarity(embedding, limit)` - Find similar documents
- `get_document_by_id(doc_id)` - Retrieve specific document
- `get_all_documents(limit)` - Get all documents
- `delete_document(doc_id)` - Delete specific document
- `clear_collection()` - Clear all documents

### ai.py - AzureOpenAIVectorModel

**Methods:**
- `create_embedding(text)` - Generate embedding for text
- `create_embeddings_batch(texts)` - Generate embeddings for multiple texts
- `generate_response(query, context_documents, system_prompt)` - RAG response generation
- `generate_streaming_response(...)` - Streaming RAG response
- `prepare_sample_data()` - Get sample documents

**Functions:**
- `setup_rag_pipeline(mongo_db, ai_model)` - Initialize everything with sample data

## Troubleshooting

### MongoDB Connection Issues
- Verify connection string format
- Check IP whitelist in MongoDB Atlas (allow your IP)
- Ensure credentials are correct
- Test with: `mongosh "mongodb+srv://..."` (if mongosh is installed)

### Azure OpenAI Issues
- Verify API key and endpoint are correct
- Check that models are deployed and accessible
- Ensure API version is compatible
- Check Azure OpenAI account quota

### Embedding Errors
- Verify text-embedding-3-small is deployed
- Check token limits (text should be reasonable length)
- Monitor API usage in Azure Portal

### Vector Search Issues
- Ensure MongoDB Atlas has Vector Search tier (paid)
- For local MongoDB, vector similarity is approximate
- Use proper vector index configuration for production

## Performance Tips

1. **Batch Operations**: Use `batch_insert_documents()` for multiple documents
2. **Batch Embeddings**: Use `create_embeddings_batch()` for multiple texts
3. **Limit Results**: Always specify limits in searches to avoid loading too much data
4. **Connection Pooling**: MongoVectorDB automatically uses connection pooling
5. **Caching**: Consider caching embeddings for frequently searched texts

## Production Deployment

For production use:

1. **Security**:
   - Store secrets in Azure Key Vault
   - Use Managed Identity instead of API keys
   - Enable network security groups

2. **Scaling**:
   - Use MongoDB Atlas with automatic scaling
   - Consider Azure OpenAI quota
   - Implement rate limiting

3. **Monitoring**:
   - Log all API calls
   - Monitor embedding creation latency
   - Track vector search performance
   - Set up alerts for errors

4. **Optimization**:
   - Implement vector caching layer
   - Use vector quantization for large datasets
   - Consider approximate nearest neighbor search
   - Batch process documents

## Next Steps

1. Set up your Azure OpenAI service
2. Create MongoDB instance
3. Configure environment variables
4. Run `python test.py` to verify setup
5. Customize sample data for your use case
6. Build your RAG application on top of this foundation

## References

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/overview/)
- [Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings)
- [RAG Pattern](https://learn.microsoft.com/azure/ai-services/openai/concepts/retrieve-augmented-generation)
