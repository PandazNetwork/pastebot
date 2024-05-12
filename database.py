from pymongo import MongoClient
from config import DB_URI, DB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(DB_URI)
        self.db = self.client[DB_NAME]
        self.users_collection = self.db["users"]

    def add_user(self, user_id):
        existing_user = self.users_collection.find_one({"user_id": user_id})
        if existing_user:
            return "User already exists"
        else:
            user_data = {"user_id": user_id}
            self.users_collection.insert_one(user_data)
            return "User added successfully"

    def get_user_by_id(self, user_id):
        return self.users_collection.find_one({"user_id": user_id})
    
    def get_all_user_ids(self):
        all_users = self.users_collection.find()
        user_ids = [user["user_id"] for user in all_users]
        return user_ids
    
    def get_total_users_count(self):
        return self.users_collection.count_documents({})
    
    def remove_user(self, user_id):
        result = self.users_collection.delete_one({"user_id": user_id})
        if result.deleted_count == 1:
            return "User removed successfully"
        else:
            return "User not found or already removed"
        
db = Database()