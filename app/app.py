"""
Main application file for MCLG-WS.
"""
from datetime import datetime
import streamlit as st
from streamlit.web import cli as stcli
import os
import sys
from pathlib import Path
# Adding .env lib methods
from dotenv import load_dotenv
import logging

# Add the project root to the Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Now import the modules
# from app.login import render_login_ui
from app.code_generation import render_code_gen_ui
from app.web_scraping import render_scraping_ui
from app.chat_integration import render_chat_ui
from app.utils.api_client import PerplexityClient
from app.config.settings import PERPLEXITY_API_KEY
from app.config.settings import APP_NAME, APP_DESCRIPTION

# if "chat_context" not in st.session_state:
#    st.session_state.chat_context = None

# if "nav_option" not in st.session_state:
#    st.session_state.nav_option = None

def main():
    """Main function to run the Streamlit application."""
    # Load environment variables
    load_dotenv()
    
    # Configure Streamlit page
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🧠",
        layout="wide"
    )

    # Sidebar header with app info
    st.sidebar.title(f"{APP_NAME}")
    st.sidebar.caption(APP_DESCRIPTION)
    
    # Check API key configuration
    if not PERPLEXITY_API_KEY:
        st.error("⚠️ Perplexity API Key not configured. Please set it in your .env file.")
        st.stop()
    
    # Initialize Perplexity client to verify connection
    try:
        perplexity = PerplexityClient()
        client = perplexity.get_client()
        
        # Display current models in sidebar
        st.sidebar.subheader("Perplexity Models")
        st.sidebar.info(f"""
        Code Generation: `{perplexity.get_model('code')}`
        Web Research: `{perplexity.get_model('web')}`
        Chat Assistant: `{perplexity.get_model('chat')}`
        """)
    except Exception as e:
        st.error(f"⚠️ Error connecting to Perplexity API: {str(e)}")
        st.stop()

    # Navigation menu
    nav_option = st.session_state.get("nav_option", None)
    if nav_option:
        menu = nav_option
        st.session_state.nav_option = None  # Reset after use
    else:
        menu = st.sidebar.selectbox(
            "Navigation",
            ["Home", "Code Generation", "Web Research", "Chat Assistant"]
        )

    # Page content based on menu selection
    if menu == "Home":
        st.title(f"{APP_NAME}: {APP_DESCRIPTION}")
        
        st.markdown("""
        Welcome to the MCLG-WS platform that combines AI-powered code generation with web research capabilities.
        
        ## Main Features:
        
        - **AI Code Generation**: Generate and extend code with AI assistance based on your project context and specific tasks;
        - **Web Research**: Extract, research and analyze web content with advanced AI tools;
        - **Chat Assistant**: Interact with an AI assistant to help with your code, research, and development tasks.
        
        This project leverages Perplexity AI's advanced models to provide high-quality results.
        
        Select a component from the sidebar to get started.
        """)
        
        # Display system status
        st.subheader("System Status")
        col1, col2 = st.columns(2)
        
        with col1:
            if PERPLEXITY_API_KEY:
                st.success("✅ Perplexity API Connected")
            else:
                st.error("❌ Perplexity API Not Connected")
                
        with col2:
            try:
                from app.utils.db_connection import DatabaseManager
                db = DatabaseManager()
                # Try to list collections to verify authentication
                collections = db.db.list_collection_names() if db.db is not None else []
                if collections:
                    st.success("✅ MongoDB Connected")
                else:
                    st.warning("⚠️ MongoDB Connected, but no collections found or access denied")
            except Exception as e:
                st.error(f"❌ MongoDB Error: {e}")
        
        # Show current time
        st.caption(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.caption("Your AI MultiCode Language & Reseaches Generator. Developed by Gabriele I Langellotto.")
    elif menu == "Web Research":
        render_scraping_ui()
    elif menu == "Code Generation":
        render_code_gen_ui()
    elif menu == "Chat Assistant":
        render_chat_ui()

if __name__ == "__main__":
    load_dotenv()
    main()