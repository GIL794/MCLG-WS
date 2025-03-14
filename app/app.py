"""
Main application file for MCLG-WS.
"""
import streamlit as st
import os
from dotenv import load_dotenv
from app.code_generation import render_code_gen_ui
from app.web_scraping import render_scraping_ui
from app.chat_integration import render_chat_ui
from app.config.settings import APP_NAME, APP_DESCRIPTION

def main():
    """Main function to run the Streamlit application"""
    # Load environment variables
    load_dotenv()
    
    # Configure Streamlit page
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🧠",
        layout="wide"
    )

    # Navigation menu
    nav_option = st.session_state.get("nav_option", None)
    if nav_option:
        menu = nav_option
        st.session_state.nav_option = None  # Reset after use
    else:
        menu = st.sidebar.selectbox(
            "Choose a Component",
            ["Home", "Code Generation", "Web Scraping", "Chat Assistant"]
        )

    # Page content based on menu selection
    if menu == "Home":
        st.title(f"{APP_NAME}: {APP_DESCRIPTION}")
        
        st.markdown("""
        Welcome to the MCLG-WS platform that combines AI-powered code generation with web scraping capabilities.
        
        ## Main Features:
        
        - **AI Code Generation**: Generate and extend code with AI assistance
        - **Web Scraping**: Scrape, analyze, and summarize web content
        - **Chat Assistant**: Interact with an AI assistant to help with your tasks
        
        Select a component from the sidebar to get started.
        """)
        
        # Display system status
        st.subheader("System Status")
        col1, col2 = st.columns(2)
        
        with col1:
            if os.getenv("OPENAI_API_KEY"):
                st.success("✅ OpenAI API Connected")
            else:
                st.error("❌ OpenAI API Not Connected")
                
        with col2:
            if os.getenv("MONGODB_URI"):
                st.success("✅ MongoDB Connected")
            else:
                st.error("❌ MongoDB Not Connected")
    
    elif menu == "Code Generation":
        render_code_gen_ui()
        
    elif menu == "Web Scraping":
        render_scraping_ui()
        
    elif menu == "Chat Assistant":
        render_chat_ui()

if __name__ == "__main__":
    main()
