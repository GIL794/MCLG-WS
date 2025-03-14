"""
Idea founded by Gabriele Iacopo Langellotto
Configuration settings for the MCLG-WS application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

# Environment settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Application settings
APP_NAME = "MCLG-WS"
APP_DESCRIPTION = "MultiCodeLanguageGeneration & WebScraping"

# MongoDB Collections
COLLECTIONS = {
    "code": "generated_code",
    "scraping": "scraped_data",
    "chat": "chat_history",
    "projects": "project_descriptions"
}

# LangChain settings
MODEL_TEMPERATURE = 0.7
