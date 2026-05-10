"""
Complete demonstration of Azure OpenAI with MongoDB Vector Database integration
Shows how to create embeddings, store them in MongoDB, and use them for RAG
"""

import sys
import os
from mongo_model import MongoVectorDB
from ai import AzureOpenAIVectorModel, setup_rag_pipeline


def main():
    """Main demonstration function"""
    
    print("=" * 60)
    print("Azure OpenAI + MongoDB Vector Database Integration Demo")
    print("=" * 60)
    
    # Initialize MongoDB connection
    print("\n1. Initializing MongoDB Vector Database...")
    try:
        mongo_db = MongoVectorDB()
        print("✓ MongoDB connected successfully")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("\nMake sure to set the MONGO_CONNECTION_STRING environment variable:")
        print("  export MONGO_CONNECTION_STRING='mongodb+srv://user:password@host/?retryWrites=true&w=majority'")
        return False
    
    # Initialize Azure OpenAI client
    print("\n2. Initializing Azure OpenAI client...")
    try:
        ai_model = AzureOpenAIVectorModel()
        print("✓ Azure OpenAI client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize Azure OpenAI: {e}")
        print("\nMake sure to set these environment variables:")
        print("  export AZURE_OPENAI_KEY='your-api-key'")
        print("  export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'")
        print("  export AZURE_OPENAI_API_VERSION='2024-05-01-preview'")
        print("  export AZURE_EMBEDDING_MODEL='text-embedding-3-small'")
        print("  export AZURE_CHAT_MODEL='gpt-4o-mini'")
        return False
    
    # Setup RAG pipeline with sample data
    print("\n3. Setting up RAG Pipeline with sample data...")
    if not setup_rag_pipeline(mongo_db, ai_model):
        print("✗ Failed to setup RAG pipeline")
        mongo_db.close()
        return False
    print("✓ RAG pipeline setup complete")
    
    # Demonstrate querying
    print("\n4. Demonstrating Vector Search and RAG...")
    query = "How do I set up Azure OpenAI with MongoDB?"
    print(f"\nQuery: '{query}'")
    print("-" * 60)
    
    try:
        # Create embedding for query
        query_embedding = ai_model.create_embedding(query)
        
        # Search for similar documents
        print("\nSearching for relevant documents...")
        similar_docs = mongo_db.search_by_similarity(query_embedding, limit=3)
        print(f"Found {len(similar_docs)} relevant documents")
        
        # Generate response using RAG
        print("\nGenerating response using RAG...")
        response = ai_model.generate_response(query, similar_docs)
        print(f"\nAssistant Response:\n{response}")
    except Exception as e:
        print(f"✗ Error during query: {e}")
        mongo_db.close()
        return False
    
    # Show all stored documents
    print("\n5. Displaying all stored documents in MongoDB...")
    print("-" * 60)
    try:
        all_docs = mongo_db.get_all_documents()
        for i, doc in enumerate(all_docs, 1):
            doc_id = doc.get("_id", "N/A")
            text_preview = doc.get("text", "")[:100] + "..."
            metadata = doc.get("metadata", {})
            print(f"\nDocument {i}:")
            print(f"  ID: {doc_id}")
            print(f"  Text: {text_preview}")
            print(f"  Metadata: {metadata}")
    except Exception as e:
        print(f"✗ Error retrieving documents: {e}")
    
    # Additional demo: Create custom embedding and query
    print("\n\n6. Custom Query Example...")
    print("-" * 60)
    custom_query = "Tell me about embeddings and vector search"
    print(f"\nQuery: '{custom_query}'")
    
    try:
        custom_embedding = ai_model.create_embedding(custom_query)
        relevant_docs = mongo_db.search_by_similarity(custom_embedding, limit=2)
        custom_response = ai_model.generate_response(custom_query, relevant_docs)
        print(f"\nAssistant Response:\n{custom_response}")
    except Exception as e:
        print(f"✗ Error in custom query: {e}")
    
    # Cleanup
    print("\n\n7. Cleaning up...")
    mongo_db.close()
    print("✓ MongoDB connection closed")
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)