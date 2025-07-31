# commented out due to login register issues

""" import bcrypt
from app.utils.db_connection import DatabaseManager

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode('utf-8'))

def register_user(username, password):
    """
#Register a new user in the MongoDB database.
"""
    db_manager = DatabaseManager()
    users_collection = db_manager.get_users_collection()

    if users_collection is None:
        return False, "Database connection failed"

    if users_collection.find_one({"username": username}):
        return False, "Username already exists"

    # Hash the password
    hashed_password = hash_password(password)

    # Insert the new user into the database
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "records": []  # Initialize with no records
    })
    return True, "User registered successfully"

def authenticate_user(username, password):
    """#Authenticate a user by checking their credentials.
"""
    db_manager = DatabaseManager()
    users_collection = db_manager.get_users_collection()

    if users_collection is None:
        return False, "Database connection failed"

    user = users_collection.find_one({"username": username})
    if not user:
        return False, "User not found"

    # Verify the password
    if check_password(password, user["password"]):
        return True, user
    else:
        return False, "Invalid password"
        """