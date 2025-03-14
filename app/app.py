import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pymongo
from pymongo import MongoClient
import scrapy
from scrapy.crawler import CrawlerProcess
import re
from bs4 import BeautifulSoup
import requests
import json

# MongoDB Connection
client = MongoClient("your-mongodb-connection-string")
db = client["mclg_ws_db"]
scraping_collection = db["scraped_data"]

# OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize LangChain for summarization
template = """
Summarize the following content scraped from a website:

{content}

Please provide a concise summary:
"""

prompt = PromptTemplate(
    input_variables=["content"],
    template=template,
)

llm = OpenAI(temperature=0.5)
summary_chain = LLMChain(llm=llm, prompt=prompt)

# Simple web scraper function
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main content (adjust selectors based on target websites)
        content = soup.find('body').get_text(separator=' ', strip=True)

        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.append({
                    'url': href,
                    'text': link.get_text(strip=True)
                })

        # Generate summary
        if len(content) > 500:
            summary = summary_chain.run(content=content[:5000])  # Limit content length
        else:
            summary = content

        return {
            'url': url,
            'content': content[:10000],  # Limit stored content
            'links': links[:20],  # Limit number of links
            'summary': summary
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e)
        }

# Streamlit UI
st.title("Web Scraping and Summarization System")

# URL input
url = st.text_input("Enter URL to scrape", "https://www.example.com")

if st.button("Scrape Website"):
    with st.spinner("Scraping in progress..."):
        result = scrape_website(url)

        if 'error' in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success("Scraping completed!")

            # Display summary
            st.subheader("AI-Generated Summary")
            st.write(result['summary'])

            # Display links
            st.subheader("Extracted Links")
            for link in result['links']:
                st.write(f"[{link['text']}]({link['url']})")

            # Save to MongoDB
            scraping_collection.insert_one(result)
            st.success("Data saved to database!")
