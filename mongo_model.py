"""
MongoDB Vector Database Model
Handles connections and operations with Azure MongoDB for vector storage
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import List, Dict, Any, Optional
import os
from datetime import datetime


class MongoVectorDB:
    """MongoDB vector database handler for storing and querying embeddings"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string. If None, uses MONGO_CONNECTION_STRING env var
        """
        if connection_string is None:
            connection_string = os.getenv("MONGO_CONNECTION_STRING")
            if not connection_string:
                raise ValueError("MongoDB connection string not provided and MONGO_CONNECTION_STRING env var not set")
        
        self.connection_string = connection_string
        self.client: Optional[MongoClient] = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
            
            # Get database and collection
            self.db = self.client["vector_database"]
            self.collection = self.db["documents"]
            
            # Create vector search index if it doesn't exist
            self._ensure_vector_index()
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _ensure_vector_index(self):
        """Ensure vector search index exists"""
        try:
            # Check if index exists
            indexes = self.collection.list_indexes()
            index_names = [idx['name'] for idx in indexes]
            
            if 'vector_index' not in index_names:
                # Create vector search index for embeddings
                self.collection.create_index([("embedding", "2dsphere")])
                print("Created vector search index")
        except Exception as e:
            print(f"Note: Vector index creation skipped: {e}")
    
    def insert_document(self, text: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Insert a document with its embedding into MongoDB
        
        Args:
            text: The original text content
            embedding: The vector embedding (list of floats)
            metadata: Additional metadata to store with the document
            
        Returns:
            The inserted document ID
        """
        document = {
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(document)
        print(f"Inserted document: {result.inserted_id}")
        return str(result.inserted_id)
    
    def batch_insert_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents at once
        
        Args:
            documents: List of documents with 'text', 'embedding', and optional 'metadata'
            
        Returns:
            List of inserted document IDs
        """
        docs_to_insert = []
        for doc in documents:
            docs_to_insert.append({
                "text": doc["text"],
                "embedding": doc["embedding"],
                "metadata": doc.get("metadata", {}),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
        
        result = self.collection.insert_many(docs_to_insert)
        print(f"Inserted {len(result.inserted_ids)} documents")
        return [str(id) for id in result.inserted_ids]
    
    def search_by_similarity(self, embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity
        Note: This is a simplified version. For production, use MongoDB Atlas Vector Search
        
        Args:
            embedding: Query embedding vector
            limit: Maximum number of results to return
            
        Returns:
            List of similar documents with their metadata
        """
        # For now, return all documents (MongoDB Atlas Vector Search would be used in production)
        results = list(self.collection.find(
            {"embedding": {"$exists": True}},
            {"embedding": 0}  # Exclude embedding for readability
        ).limit(limit))
        
        return results
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID
        
        Args:
            doc_id: The document ID
            
        Returns:
            The document or None if not found
        """
        from bson import ObjectId
        try:
            doc = self.collection.find_one({"_id": ObjectId(doc_id)}, {"embedding": 0})
            return doc
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return None
    
    def get_all_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all documents from the collection
        
        Args:
            limit: Maximum number of documents to retrieve
            
        Returns:
            List of documents
        """
        return list(self.collection.find({}, {"embedding": 0}).limit(limit))
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document by its ID
        
        Args:
            doc_id: The document ID
            
        Returns:
            True if document was deleted, False otherwise
        """
        from bson import ObjectId
        try:
            result = self.collection.delete_one({"_id": ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        result = self.collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents")
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
