"""
Code generation module using Perplexity API.
"""
import logging
import os
import streamlit as st
from streamlit.web import cli as stcli
from datetime import datetime
from app.utils.api_client import PerplexityClient
from app.utils.db_connection import DatabaseManager
from app.config.settings import COLLECTIONS
import unittest
import re

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
                temperature=0.2,  # Lowered temperature for more deterministic code
                max_tokens=1500   # Allow for shorter, precise code generation
            )
            
            if "error" in response:
                return f"Error: {response['error']}"
            
            generated_code = response["content"]
            
            # Save to database if connection exists
            if self.db is not None:
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
            logging.error(f"Error generating code: {str(e)}")
            return f"Error: {str(e)}"

def extract_code_from_response(response_text):
    """Extract Python code block from AI response."""
    code_blocks = re.findall(r"```python(.*?)```", response_text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    # Fallback: try to find any code block
    code_blocks = re.findall(r"```(.*?)```", response_text, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return response_text.strip()  # If no code block, return all

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
        
        with st.spinner("AI working on the code... This may take a moment."):
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
            code_only = extract_code_from_response(generated_code)
            show_thinking = st.checkbox("Show AI thinking and explanation", value=False)
            if show_thinking:
                st.markdown("#### Full AI Response (including reasoning):")
                st.write(generated_code)
            st.markdown("#### Generated Python Code:")
            st.code(code_only, language="python")
            st.session_state.code_context = code_only

            # Add button to discuss with AI
            if st.button("Discuss with AI Assistant"):
                st.session_state.chat_context = f"Generated code: {generated_code}"
                st.session_state.nav_option = "Chat Assistant"
                st.write("Redirecting to Chat Assistant...")  # Debug message
                st.experimental_rerun()

class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.code_gen = CodeGenerator()

    def test_generate_code_success(self):
        result = self.code_gen.generate_code(
            project_context="A Python project",
            existing_code="def hello_world(): print('Hello, World!')",
            task="Add a function to calculate the factorial of a number."
        )
        self.assertIn("def factorial", result)

    def test_generate_code_error(self):
        result = self.code_gen.generate_code(
            project_context="",
            existing_code="",
            task=""
        )
        self.assertTrue(result.startswith("Error:"))

if __name__ == "__main__":
    unittest.main()
