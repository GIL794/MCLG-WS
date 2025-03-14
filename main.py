"""
MCLG-WS: MultiCodeLanguageGeneration & WebScraping
Main entry point for the application.

Idea founded by Gabriele Iacopo Langellotto

This file acts as the entry point and simply imports and runs the main
function from the app module.
"""
import sys
import os
from pathlib import Path

# Add the current directory to Python's path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the main function from app module
from app.app import main

if __name__ == "__main__":
    # Run the Streamlit application
    main()









































# Idea founded by Gabriele Iacopo Langellotto
