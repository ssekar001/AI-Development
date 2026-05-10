"""
OpenAI Vector Database Integration
Creates embeddings and uses them for retrieval-augmented generation (RAG)
"""

from openai import AzureOpenAI
from typing import List, Dict, Any, Optional
import os
import json


class AzureOpenAIVectorModel:
    """Azure OpenAI model for creating embeddings and generating responses using RAG"""
    
    def __init__(self):
        """Initialize Azure OpenAI client with environment variables"""
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        self.embedding_model = os.getenv("AZURE_EMBEDDING_MODEL", "text-embedding-3-small")
        self.chat_model = os.getenv("AZURE_CHAT_MODEL", "gpt-4o-mini")
        
        # Validate required environment variables
        if not os.getenv("AZURE_OPENAI_KEY"):
            raise ValueError("AZURE_OPENAI_KEY environment variable not set")
        if not os.getenv("AZURE_OPENAI_ENDPOINT"):
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable not set")
        
        print("Azure OpenAI client initialized successfully")
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding for the given text
        
        Args:
            text: The text to create an embedding for
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            embedding = response.data[0].embedding
            print(f"Created embedding with {len(embedding)} dimensions")
            return embedding
        except Exception as e:
            print(f"Error creating embedding: {e}")
            raise
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts at once
        
        Args:
            texts: List of texts to create embeddings for
            
        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            # Sort by index to maintain order
            embeddings = sorted(response.data, key=lambda x: x.index)
            return [item.embedding for item in embeddings]
        except Exception as e:
            print(f"Error creating batch embeddings: {e}")
            raise
    
    def generate_response(self, query: str, context_documents: List[Dict[str, Any]], 
                         system_prompt: Optional[str] = None) -> str:
        """
        Generate a response using RAG (Retrieval-Augmented Generation)
        
        Args:
            query: The user's query
            context_documents: Retrieved documents to use as context
            system_prompt: Optional custom system prompt
            
        Returns:
            The generated response from the model
        """
        # Build context from documents
        context = "\n\n".join([
            f"Document {i+1}:\n{doc.get('text', '')}\n"
            f"Metadata: {json.dumps(doc.get('metadata', {}), indent=2)}"
            for i, doc in enumerate(context_documents[:5])  # Limit to 5 documents
        ])
        
        # Default system prompt for RAG
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant that answers questions based on provided documents.
Use the provided context to answer the user's question accurately.
If the information is not in the provided context, you can say so but try to be helpful.
Be concise and clear in your responses."""
        
        # Build the message
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", 
                "content": f"Context documents:\n\n{context}\n\nQuestion: {query}"
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            raise
    
    def generate_streaming_response(self, query: str, context_documents: List[Dict[str, Any]],
                                   system_prompt: Optional[str] = None):
        """
        Generate a streaming response using RAG
        
        Args:
            query: The user's query
            context_documents: Retrieved documents to use as context
            system_prompt: Optional custom system prompt
            
        Yields:
            Chunks of the response as they are generated
        """
        # Build context from documents
        context = "\n\n".join([
            f"Document {i+1}:\n{doc.get('text', '')}\n"
            f"Metadata: {json.dumps(doc.get('metadata', {}), indent=2)}"
            for i, doc in enumerate(context_documents[:5])
        ])
        
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant that answers questions based on provided documents.
Use the provided context to answer the user's question accurately.
If the information is not in the provided context, you can say so but try to be helpful.
Be concise and clear in your responses."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", 
                "content": f"Context documents:\n\n{context}\n\nQuestion: {query}"
            }
        ]
        
        try:
            with self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            ) as response:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error generating streaming response: {e}")
            raise
    
    def prepare_sample_data(self) -> List[Dict[str, Any]]:
        """
        Prepare sample data for demonstration
        
        Returns:
            List of sample documents with text and metadata
        """
        sample_texts = [
            {
                "text": "Azure OpenAI Service provides REST API access to OpenAI's powerful language models including the GPT-4, GPT-4 Turbo, and GPT-3.5-Turbo models. These models can be easily adapted to your specific task including content generation, summarization, semantic search, and natural language to code translation.",
                "metadata": {"source": "Azure OpenAI Documentation", "category": "overview"}
            },
            {
                "text": "Vector embeddings are numerical representations of text that capture semantic meaning. Azure OpenAI provides the text-embedding-3-small and text-embedding-3-large models for generating high-quality embeddings. These embeddings can be used for semantic search, clustering, and similarity comparisons.",
                "metadata": {"source": "Embeddings Guide", "category": "embeddings"}
            },
            {
                "text": "MongoDB Atlas Vector Search allows you to perform semantic searches on your data using vector embeddings. It integrates seamlessly with Azure OpenAI to enable powerful AI-driven search experiences. You can index vector fields and perform approximate nearest neighbor searches efficiently.",
                "metadata": {"source": "MongoDB Documentation", "category": "vector-search"}
            },
            {
                "text": "Retrieval-Augmented Generation (RAG) is a technique that combines large language models with external knowledge sources. It retrieves relevant documents from a knowledge base and provides them as context to the language model, enabling more accurate and up-to-date responses.",
                "metadata": {"source": "AI Best Practices", "category": "rag"}
            },
            {
                "text": "To get started with Azure OpenAI and MongoDB integration, first set up your Azure OpenAI resource, configure authentication, prepare your MongoDB instance with vector search capability, then create embeddings for your data and store them in your MongoDB database.",
                "metadata": {"source": "Getting Started Guide", "category": "setup"}
            }
        ]
        
        return sample_texts


def setup_rag_pipeline(mongo_db, ai_model: AzureOpenAIVectorModel) -> bool:
    """
    Setup the complete RAG pipeline with sample data
    
    Args:
        mongo_db: MongoVectorDB instance
        ai_model: AzureOpenAIVectorModel instance
        
    Returns:
        True if setup successful
    """
    try:
        print("\n=== Setting up RAG Pipeline ===\n")
        
        # Get sample data
        sample_data = ai_model.prepare_sample_data()
        print(f"Prepared {len(sample_data)} sample documents")
        
        # Create embeddings for each document
        texts = [doc["text"] for doc in sample_data]
        print("Creating embeddings for sample documents...")
        embeddings = ai_model.create_embeddings_batch(texts)
        
        # Prepare documents with embeddings
        docs_to_insert = []
        for doc, embedding in zip(sample_data, embeddings):
            docs_to_insert.append({
                "text": doc["text"],
                "embedding": embedding,
                "metadata": doc["metadata"]
            })
        
        # Insert into MongoDB
        print("Inserting documents into MongoDB...")
        inserted_ids = mongo_db.batch_insert_documents(docs_to_insert)
        print(f"Successfully inserted {len(inserted_ids)} documents into MongoDB\n")
        
        return True
    except Exception as e:
        print(f"Error setting up RAG pipeline: {e}")
        return False
