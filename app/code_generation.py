"""
Code generation module using LangChain and OpenAI.
"""
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from datetime import datetime
from app.utils.db_connection import DatabaseManager
from app.config.settings import MODEL_TEMPERATURE, COLLECTIONS

class CodeGenerator:
    def __init__(self):
        # Initialize LangChain components
        self.llm = OpenAI(temperature=MODEL_TEMPERATURE)
        self.prompt = PromptTemplate(
            template="""You are a helpful AI coding assistant. Based on the following:
            Project Context: {project_context}
            Existing Code: {existing_code}
            Task: {task}
            Generate Python code:""",
            input_variables=["project_context", "existing_code", "task"]
        )
        self.code_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        # Get database collection
        db_manager = DatabaseManager()
        self.db = db_manager.get_collection(COLLECTIONS["code"])

    def generate_code(self, project_context, existing_code, task):
        """Generate code based on input parameters"""
        try:
            result = self.code_chain.run(
                project_context=project_context,
                existing_code=existing_code,
                task=task
            )
            
            # Save to database if connection exists
            if self.db:
                self.db.insert_one({
                    "project_context": project_context,
                    "existing_code": existing_code,
                    "task": task,
                    "generated_code": result,
                    "timestamp": datetime.utcnow()
                })
            
            return result
        except Exception as e:
            print(f"Error generating code: {e}")
            return f"Error: {str(e)}"

def render_code_gen_ui():
    """Render the code generation UI in Streamlit"""
    st.title("AI Code Generation")
    
    with st.form("code_gen_form"):
        project_context = st.text_area(
            "Project Context", 
            placeholder="Describe your project needs"
        )
        
        existing_code = st.text_area(
            "Existing Code (optional)", 
            placeholder="Paste any existing code here"
        )
        
        task = st.text_area(
            "Development Task", 
            placeholder="What code do you need the AI to generate?"
        )
        
        submitted = st.form_submit_button("Generate Code")
        
    if submitted:
        with st.spinner("Generating code..."):
            code_gen = CodeGenerator()
            generated_code = code_gen.generate_code(
                project_context=project_context,
                existing_code=existing_code,
                task=task
            )
            
            st.code(generated_code, language="python")
            st.success("Code generated and saved to database!")
            
            # Save to session state for sharing with chat
            st.session_state.code_context = generated_code
            
            # Add button to discuss with AI
            if st.button("Discuss with AI Assistant"):
                st.session_state.chat_context = f"Generated code: {generated_code}"
                st.session_state.nav_option = "Chat Assistant"
                st.experimental_rerun()
