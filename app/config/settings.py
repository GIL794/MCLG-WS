"""
Idea founded by Gabriele Iacopo Langellotto
Configuration settings for the MCLG-WS application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application info
APP_NAME = "MCLG-WS"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "MultiCodeLanguageGeneration & WebScraping"

# Perplexity API Configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_BASE_URL = os.getenv("PERPLEXITY_BASE_URL", "https://api.perplexity.ai")

# Model configuration
PERPLEXITY_MODELS = {
    "code": "sonar-reasoning-pro",  # For code generation
    "web": "sonar-deep-research",   # For web scraping
    "chat": "sonar-pro"             # For chat assistant
}

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "mclg_ws_db"

# Collection names
COLLECTIONS = {
    "code": "generated_code",
    "scraping": "scraped_data",
    "chat": "chat_history",
    "projects": "project_descriptions"
}

# Environment and debug settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
