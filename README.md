# Azure OpenAI + MongoDB Vector Database Integration - Complete Solution

## Project Overview

This solution provides a complete implementation for integrating Azure OpenAI's embedding and chat models with MongoDB for vector-based retrieval-augmented generation (RAG). It allows you to:

✓ Store documents with vector embeddings in MongoDB  
✓ Create OpenAI embeddings from your data  
✓ Perform semantic similarity searches  
✓ Generate AI responses using retrieved documents as context  
✓ Scale your AI applications with vector database capabilities  

## Files Created

### Core Implementation Files

1. **mongo_model.py** - MongoDB Vector Database Handler
   - `MongoVectorDB` class for database operations
   - Methods for inserting, searching, and managing documents
   - Vector similarity search capabilities
   - Batch operations for efficiency

2. **ai.py** - Azure OpenAI Integration
   - `AzureOpenAIVectorModel` class for AI operations
   - Embedding creation (single and batch)
   - RAG-based response generation
   - Streaming response support
   - Sample data preparation

3. **test.py** - Complete Demonstration
   - Full end-to-end workflow example
   - MongoDB connection setup
   - Sample data loading with embeddings
   - Query execution with RAG
   - Results display and cleanup

### Configuration Files

4. **requirements.txt** - Python Dependencies
   - All necessary packages with version specifications
   - pymongo, openai, azure-identity, azure-ai-projects

5. **.env.template** - Environment Variable Template
   - Copy to `.env` and fill in your credentials
   - MongoDB connection string
   - Azure OpenAI API key, endpoint, models

### Documentation

6. **SETUP_GUIDE.md** - Complete Setup Instructions
   - Step-by-step installation guide
   - Configuration walkthrough
   - Usage examples
   - Troubleshooting tips
   - Performance optimization
   - Production deployment checklist

## Quick Start

### 1. Set Up Environment Variables

```bash
# Copy template and update with your credentials
cp .env.template .env
# Edit .env with your MongoDB and Azure OpenAI credentials
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Demo

```bash
python test.py
```

## Architecture

```
User Query
    │
    ├──► Create Embedding (Azure OpenAI)
    │         │
    │         └──► MongoDB Vector Search
    │                  │
    │                  └──► Retrieve Similar Documents
    │                          │
    └─────────────────────────►├──► Generate Response (RAG)
                               │
                               └──► Return to User
```

## Key Features

### Vector Embedding Management
- Create embeddings for documents and queries
- Batch process multiple texts efficiently
- Store embeddings with metadata in MongoDB

### Semantic Search
- Find similar documents using vector similarity
- Configurable result limits
- Flexible query capabilities

### Retrieval-Augmented Generation (RAG)
- Generate AI responses based on retrieved context
- Customizable system prompts
- Support for streaming responses
- Maintains conversation context

### Production Ready
- Error handling and logging
- Context manager support for resource cleanup
- Batch operations for performance
- Configuration via environment variables

## Usage Examples

### Basic RAG Workflow

```python
from mongo_model import MongoVectorDB
from ai import AzureOpenAIVectorModel

# Initialize
mongo_db = MongoVectorDB()
ai_model = AzureOpenAIVectorModel()

# Create embedding for query
query = "How to set up Azure OpenAI?"
embedding = ai_model.create_embedding(query)

# Search for relevant documents
docs = mongo_db.search_by_similarity(embedding, limit=3)

# Generate response with context
response = ai_model.generate_response(query, docs)
print(response)
```

### Insert Documents with Embeddings

```python
# Create embeddings
texts = ["Document 1", "Document 2", "Document 3"]
embeddings = ai_model.create_embeddings_batch(texts)

# Prepare documents
docs = [
    {"text": text, "embedding": emb, "metadata": {"source": "docs"}}
    for text, emb in zip(texts, embeddings)
]

# Insert into MongoDB
ids = mongo_db.batch_insert_documents(docs)
```

## Environment Variables Required

```
MONGO_CONNECTION_STRING=mongodb+srv://user:pass@host/?retryWrites=true&w=majority
AZURE_OPENAI_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-05-01-preview
AZURE_EMBEDDING_MODEL=text-embedding-3-small
AZURE_CHAT_MODEL=gpt-4o-mini
```

## Configuration Options

### MongoDB
- **Collection**: `documents` (in `vector_database` database)
- **Fields**: `text`, `embedding`, `metadata`, `created_at`, `updated_at`
- **Indexes**: Automatic vector search index creation

### Azure OpenAI
- **Embedding Model**: text-embedding-3-small (1536 dimensions)
- **Chat Model**: gpt-4o-mini
- **API Version**: 2024-05-01-preview

## Performance Considerations

1. **Batch Operations**: Use batch methods for multiple documents
2. **Result Limits**: Always specify limits in searches
3. **Caching**: Consider caching embeddings for frequently used texts
4. **Connection Pooling**: MongoDB client uses automatic connection pooling
5. **Vector Indexing**: For production, enable MongoDB Atlas Vector Search

## Troubleshooting

**MongoDB Connection Failed**
- Check connection string format
- Verify IP whitelist in MongoDB Atlas
- Test credentials with mongosh

**Azure OpenAI Errors**
- Verify API key and endpoint
- Check model deployments exist
- Monitor Azure OpenAI account quota

**Embedding Errors**
- Verify text-embedding-3-small is deployed
- Check text length (reasonable limits)
- Monitor API usage

**Vector Search Issues**
- For production, upgrade to Atlas Vector Search tier
- Local MongoDB uses approximate similarity
- Implement proper vector indexes

## Next Steps

1. **Customize**: Modify `prepare_sample_data()` with your own documents
2. **Scale**: Use batch operations for production datasets
3. **Optimize**: Configure vector search indexes for large datasets
4. **Monitor**: Implement logging and monitoring
5. **Deploy**: Move to production with Key Vault secrets

## Security Best Practices

- Store secrets in Azure Key Vault (not in .env)
- Use Managed Identity instead of API keys in production
- Enable network security groups
- Implement rate limiting
- Log all API calls
- Monitor for suspicious activity

## Support & Documentation

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/)
- [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [RAG Pattern](https://learn.microsoft.com/azure/ai-services/openai/concepts/retrieve-augmented-generation)

## Files Summary

| File | Purpose | Status |
|------|---------|--------|
| mongo_model.py | MongoDB operations | ✓ Complete |
| ai.py | Azure OpenAI integration | ✓ Complete |
| test.py | End-to-end demo | ✓ Complete |
| requirements.txt | Dependencies | ✓ Complete |
| .env.template | Configuration template | ✓ Complete |
| SETUP_GUIDE.md | Setup instructions | ✓ Complete |
| README.md | This file | ✓ Complete |

## Ready to Use

Everything is set up and ready to go! Just:

1. Fill in your `.env` file with Azure and MongoDB credentials
2. Run `python test.py` to verify everything works
3. Customize the code for your specific use case
4. Deploy to production with proper security measures

Happy coding! 🚀
