"""
Database connection utility for MongoDB.
"""
import os
import pymongo
from pymongo import MongoClient
from app.config.settings import MONGODB_URI

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.initialize_connection()
        return cls._instance
    
    def initialize_connection(self):
        """Initialize the MongoDB connection"""
        try:
            # Check if MongoDB URI is set
            if not MONGODB_URI:
                print("Warning: MongoDB URI is not set in environment variables")
                self.client = None
                self.db = None
                return
            
            # Create MongoDB client
            self.client = MongoClient(MONGODB_URI)
            
            # Test connection
            self.client.admin.command('ping')
            print("Connected successfully to MongoDB")
            
            # Set database
            self.db = self.client["mclg_ws_db"]
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None
    
    def get_collection(self, collection_name):
        """Get a MongoDB collection by name"""
        if self.db:
            return self.db[collection_name]
        return None
