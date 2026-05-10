import os
from pymongo import MongoClient

# Get connection string from environment variable
connection_string = os.getenv("MONGO_CONNECTION_STRING")
if not connection_string:
    print("Error: MONGO_CONNECTION_STRING environment variable not set")
    print("Please set it like: export MONGO_CONNECTION_STRING='mongodb+srv://username:password@cluster.mongodb.net/'")
    exit(1)

client = MongoClient(connection_string)

# Test connection
try:
    print("Testing connection...")
    print(client.list_database_names())
    print("Connected successfully")
except Exception as e:
    print(f"Connection failed: {e}")