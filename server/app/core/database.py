import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smartpass")

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully")
except ServerSelectionTimeoutError:
    print("Warning: Could not connect to MongoDB. Make sure MongoDB is running at", MONGODB_URL)
    client = MongoClient(MONGODB_URL)

db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
subjects_collection = db["subjects"]
classes_collection = db["classes"]
attendances_collection = db["attendances"]

# Create indexes for better query performance
users_collection.create_index("email", unique=True)
subjects_collection.create_index("code", unique=True)
attendances_collection.create_index([("user_id", 1), ("class_id", 1), ("timestamp", 1)])

def get_db():
    """Return database instance"""
    return db

def close_db():
    """Close database connection"""
    client.close()
