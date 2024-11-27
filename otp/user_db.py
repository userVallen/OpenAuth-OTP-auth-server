from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Loads environment variables from .env
load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')

# Connect to the user database
client = MongoClient(mongodb_uri)
db = client['auth-db']

# Access the 'users' collection
users_collection = db['users']
counters_collection = db['counters']

def check_user(username):
    # Find the user by username
    user_data = users_collection.find_one({"username": username})

    if user_data is None:
        return "Not Found"
    else:
        return "Found"

def store_hashed_key(username, key):
    # Check if user already exists
    if users_collection.find_one({"username": username}):
        # Store the key in the 'key' field
        result = users_collection.update_one(
            {"username": username},  # Find user by username
            {"$set": {"key": key}}  # Set the key field
        )

        if result.modified_count > 0:
            return "Key updated successfully"
        else:
            return "Key was not updated"
    else:
        return "User not found"

def get_hashed_key(username):
    # Check if the user exists
    user_data = users_collection.find_one({"username": username})

    if user_data:
        return user_data.get('key', None)
    else:
        return "User not found"
