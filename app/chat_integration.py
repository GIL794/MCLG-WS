"""
Chat integration module using Perplexity API.
"""
import os
import streamlit as st
from streamlit.web import cli as stcli
from datetime import datetime
from app.utils.api_client import PerplexityClient
from app.utils.db_connection import DatabaseManager
from app.config.settings import COLLECTIONS

class ChatAssistant:
    def __init__(self):
        # Initialize Perplexity client
        perplexity = PerplexityClient()
        self.client = perplexity.get_client()
        self.model = perplexity.get_model("chat")  # sonar-pro
        
        # Get database collection
        db_manager = DatabaseManager()
        self.db = db_manager.get_collection(COLLECTIONS["chat"])
        
        # Initialize chat history if none exists
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are a helpful AI assistant for the MCLG-WS system, which helps with code generation and web research."}
            ]
    
    def process_message(self, user_message, context=None):
        """Process a user message and return the AI response."""
        try:
            # Add context to the system message if provided
            if context:
                system_message = {
                    "role": "system", 
                    "content": f"You are a helpful AI assistant for the MCLG-WS system. Consider this context information: {context}"
                }
                # Update the system message
                if st.session_state.messages["role"] == "system":
                    st.session_state.messages = system_message
                else:
                    st.session_state.messages.insert(0, system_message)
                    
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_message})
            
            # Get response from Perplexity
            perplexity = PerplexityClient()
            response = perplexity.generate_completion(
                model=self.model,
                messages=st.session_state.messages,
                temperature=0.7,  # Standard temperature for conversational responses
                max_tokens=2000   # Allow for detailed responses
            )
            
            if "error" in response:
                return f"Error: {response['error']}"
            
            ai_response = response["content"]
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Save to database if connection exists
            if self.db:
                self.db.insert_one({
                    "user_message": user_message,
                    "context": context,
                    "ai_response": ai_response,
                    "model": response["model"],
                    "token_usage": response["usage"],
                    "timestamp": datetime.utcnow()
                })
            
            return ai_response
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return f"Error: {str(e)}"

def render_chat_ui():
    """Render the chat UI in Streamlit."""
    st.title("AI Chat Assistant")
    
    # Initialize chat history in session state if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["is_user"]:
            st.write(f"🧑 **You**: {message['text']}")
        else:
            st.write(f"🤖 **AI**: {message['text']}")
    
    # Check for context in session state
    context = st.session_state.get("chat_context", None)
    if context:
        st.info(f"Using context: {context[:100]}..." + ("" if len(context) <= 100 else "..."))
    
    # Get user input
    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_input("Type your message:", key="chat_input")
        submitted = st.form_submit_button("Send")
    
    if submitted and user_message:
        # Create chat assistant
        chat_assistant = ChatAssistant()
        
        # Add user message to chat history
        st.session_state.chat_history.append({
            "is_user": True,
            "text": user_message
        })
        
        # Get AI response
        with st.spinner("AI is thinking..."):
            response = chat_assistant.process_message(user_message, context)
        
        # Add AI response to chat history
        st.session_state.chat_history.append({
            "is_user": False,
            "text": response
        })
        
        # Clear context after use
        if context:
            st.session_state.chat_context = None
        
        # Force refresh
        st.experimental_rerun()
