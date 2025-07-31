"""
Database connection utility for MongoDB.
"""
import unittest
from pymongo import MongoClient
from app.config.settings import MONGODB_URI, DB_NAME
import streamlit as st

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.initialize_connection()
        return cls._instance

    def initialize_connection(self):
        """Initialize connection to MongoDB."""
        try:
            # Check if MongoDB URI is set
            if not MONGODB_URI:
                print("Warning: MongoDB URI is not set in environment variables")
                self.client = None
                self.db = None
                return

            # Create MongoDB client size-capped to manage connections efficiently
            self.client = MongoClient(MONGODB_URI, maxPoolSize=50, minPoolSize=10)

            # Ping database to test connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB")

            # Set database
            self.db = self.client[DB_NAME]

        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        """Get any collection by name from the MongoDB database."""
        if self.db is not None:
            return self.db[collection_name]
        print("Warning: Database not connected, returning None")
        return None
    
    def close_connection(self):
        """Close the MongoDB connection."""
        if self.client is None:
            self.client.close()
            print("MongoDB connection closed")

#@st.cache_data
#def get_user_records(username):
 #   users_collection = db_manager.get_users_collection()
  #  return users_collection.find_one({"username": username})

class TestDatabaseManager(unittest.TestCase):
    def test_database_connection(self):
        db_manager = DatabaseManager()
        self.assertIsNotNone(db_manager.db)

if __name__ == "__main__":
    unittest.main()
