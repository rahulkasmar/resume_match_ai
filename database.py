# database.py
from pymongo import MongoClient
from config import MONGO_URI

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Select the database from the URI
db = client.get_database() 

# Collections
users_collection = db["users"]
notes_collection = db["notes"]
analysis_results_collection = db["analysis_results"] 

print("✅ Connected to MongoDB")


# --- ADD THESE FUNCTIONS ---

def get_user_collection():
    """Returns the users collection instance."""
    return users_collection

def get_notes_collection():
    """Returns the notes collection instance."""
    return notes_collection
def get_analysis_collection(): # <-- ADD THIS FUNCTION
    """Returns the analysis_results collection instance."""
    return analysis_results_collection