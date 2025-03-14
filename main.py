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

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Now import the app module
from app.app import main

if __name__ == "__main__":
    # Run the Streamlit application
    main()









































# Idea founded by Gabriele Iacopo Langellotto
