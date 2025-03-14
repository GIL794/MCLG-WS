import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pymongo
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("your-mongodb-connection-string")
db = client["mclg_ws_db"]
code_collection = db["generated_code"]
project_collection = db["project_descriptions"]

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize LangChain
template = """
You are a helpful AI coding assistant. Based on the following code or description, 
please help generate or extend the code as needed.

Project Context: {project_description}
Existing Code: {existing_code}
Task: {task}

Please generate the code in Python:
"""

prompt = PromptTemplate(
    input_variables=["project_description", "existing_code", "task"],
    template=template,
)

llm = OpenAI(temperature=0.7)
code_chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit UI
st.title("AI Code Generation System")

# Project description
project_description = st.text_area(
    "Project Description",
    "MultiCodeLanguageGeneration & WebScraping AI project"
)

# Existing code
existing_code = st.text_area("Existing Code (if any)", "")

# Task description
task = st.text_area(
    "What do you want the AI to help with?",
    "Generate a function to scrape data from a website"
)

if st.button("Generate Code"):
    result = code_chain.run(
        project_description=project_description,
        existing_code=existing_code,
        task=task
    )

    st.code(result, language="python")

    # Save to MongoDB
    code_entry = {
        "project_description": project_description,
        "existing_code": existing_code,
        "task": task,
        "generated_code": result,
        "timestamp": pymongo.datetime.datetime.utcnow()
    }

    code_collection.insert_one(code_entry)
    st.success("Code generated and saved to database!")
