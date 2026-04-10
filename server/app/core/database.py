from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import certifi
from .config import MONGODB_URL, DATABASE_NAME


def _create_client() -> MongoClient:
    kwargs = {"serverSelectionTimeoutMS": 15000}
    # Atlas SRV connections require TLS and often need an explicit CA bundle in hosted environments.
    if MONGODB_URL.startswith("mongodb+srv://"):
        kwargs.update({"tls": True, "tlsCAFile": certifi.where()})
    return MongoClient(MONGODB_URL, **kwargs)


try:
    client = _create_client()
    # Verify connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully")
except ServerSelectionTimeoutError:
    print("Warning: Could not connect to MongoDB. Make sure MongoDB is running at", MONGODB_URL)
    client = _create_client()

db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
subjects_collection = db["subjects"]
classes_collection = db["classes"]
attendances_collection = db["attendances"]

# Create indexes for better query performance
try:
    users_collection.create_index("email", unique=True)
    subjects_collection.create_index("code", unique=True)
    attendances_collection.create_index([("user_id", 1), ("class_id", 1), ("timestamp", 1)])
except ServerSelectionTimeoutError as exc:
    print(f"Warning: Skipping index creation because MongoDB is unreachable: {exc}")

def get_db():
    """Return database instance"""
    return db

def close_db():
    """Close database connection"""
    client.close()
