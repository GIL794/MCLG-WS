"""
Code generation module using Perplexity API.
"""
import os
import streamlit as st
from streamlit.web import cli as stcli
from datetime import datetime
from app.utils.api_client import PerplexityClient
from app.utils.db_connection import DatabaseManager
from app.config.settings import COLLECTIONS

class CodeGenerator:
    def __init__(self):
        # Initialize Perplexity client
        perplexity = PerplexityClient()
        self.client = perplexity.get_client()
        self.model = perplexity.get_model("code")  # sonar-reasoning-pro
        
        # Get database collection
        db_manager = DatabaseManager()
        self.db = db_manager.get_collection(COLLECTIONS["code"])
    
    def generate_code(self, project_context, existing_code, task):
        """Generate code using Perplexity API."""
        try:
            # Construct prompt for code generation
            messages = [
                {"role": "system", "content": "You are an expert software developer who writes clear, well-documented code."},
                {"role": "user", "content": f"""
                Please generate Python code based on the following information:
                
                PROJECT CONTEXT:
                {project_context}
                
                EXISTING CODE (if any):
                '''
                {existing_code}
                '''
                
                TASK:
                {task}
                
                Please write complete, well-documented Python code that implements this task.
                Include detailed comments explaining how the code works.
                """}
            ]
            
            # Get response from Perplexity
            perplexity = PerplexityClient()
            response = perplexity.generate_completion(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more deterministic code
                max_tokens=3000   # Allow for longer code generation
            )
            
            if "error" in response:
                return f"Error: {response['error']}"
            
            generated_code = response["content"]
            
            # Save to database if connection exists
            if self.db:
                self.db.insert_one({
                    "project_context": project_context,
                    "existing_code": existing_code,
                    "task": task,
                    "generated_code": generated_code,
                    "model": response["model"],
                    "token_usage": response["usage"],
                    "timestamp": datetime.utcnow()
                })
            
            return generated_code
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return f"Error: {str(e)}"

def render_code_gen_ui():
    """Render the code generation UI in Streamlit."""
    st.title("AI Code Generation")
    
    with st.form("code_gen_form"):
        project_context = st.text_area(
            "Project Context", 
            placeholder="Describe your project needs and requirements",
            height=150
        )
        
        existing_code = st.text_area(
            "Existing Code (optional)", 
            placeholder="Paste any existing code here that the AI should build upon",
            height=200
        )
        
        task = st.text_area(
            "Development Task", 
            placeholder="Describe the specific coding task you need help with",
            height=150
        )
        
        submitted = st.form_submit_button("Generate Code")
    
    if submitted:
        if not project_context or not task:
            st.error("Please provide both project context and task description")
            return
            
        with st.spinner("Generating code... This may take a moment."):
            code_gen = CodeGenerator()
            generated_code = code_gen.generate_code(
                project_context=project_context,
                existing_code=existing_code,
                task=task
            )
            
            if generated_code.startswith("Error:"):
                st.error(generated_code)
            else:
                st.success("Code generation completed!")

                code_parts = generated_code.split("python")
                # Clean up the code if needed
                try:
                    if type(code_parts[0]) == 'str'
                        # Extract code from markdown code blocks
                        if len(code_parts) > 1:
                            code_block = code_parts[1].split("")
                            generated_code = code_block
                except:
                    print("If statement crush")
                # Display the generated code
                st.code(generated_code, language="python")
                
                # Save to session state for sharing with chat
                st.session_state.code_context = generated_code
                
                # Add button to discuss with AI
                if st.button("Discuss with AI Assistant"):
                    st.session_state.chat_context = f"Generated code: {generated_code}"
                    st.session_state.nav_option = "Chat Assistant"
                    st.experimental_rerun() 
