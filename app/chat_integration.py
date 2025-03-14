"""
Chat integration module using LangChain.
"""
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from datetime import datetime
from app.utils.db_connection import DatabaseManager
from app.config.settings import MODEL_TEMPERATURE, COLLECTIONS

class ChatAssistant:
    def __init__(self):
        # Initialize LangChain components
        self.llm = OpenAI(temperature=MODEL_TEMPERATURE)
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        
        # Get database collection
        db_manager = DatabaseManager()
        self.db = db_manager.get_collection(COLLECTIONS["chat"])

    def process_message(self, user_message, context=None):
        """Process a user message and return the AI response"""
        try:
            # Add context if provided
            if context:
                enhanced_message = f"Context information: {context}\n\nUser question: {user_message}"
            else:
                enhanced_message = user_message
                
            # Get response from conversation chain
            response = self.conversation.predict(input=enhanced_message)
            
            # Save to database if connection exists
            if self.db:
                self.db.insert_one({
                    "user_message": user_message,
                    "context": context,
                    "ai_response": response,
                    "timestamp": datetime.utcnow()
                })
            
            return response
        except Exception as e:
            print(f"Error processing message: {e}")
            return f"Error: {str(e)}"

def render_chat_ui():
    """Render the chat UI in Streamlit"""
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
        st.info(f"Using context: {context[:100]}...")
    
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
