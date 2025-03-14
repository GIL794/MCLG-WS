"""
Web scraping module using BeautifulSoup and LangChain.
"""
import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from datetime import datetime
from app.utils.db_connection import DatabaseManager
from app.config.settings import MODEL_TEMPERATURE, COLLECTIONS

class WebScraper:
    def __init__(self):
        # Initialize LangChain for summarization
        self.llm = OpenAI(temperature=MODEL_TEMPERATURE)
        self.prompt = PromptTemplate(
            template="""Summarize the following content:
            {content}
            
            Provide a concise summary:""",
            input_variables=["content"]
        )
        self.summary_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        # Get database collection
        db_manager = DatabaseManager()
        self.db = db_manager.get_collection(COLLECTIONS["scraping"])

    def scrape_website(self, url):
        """Scrape website and generate summary"""
        try:
            # Send request to the website
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
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
                summary = self.summary_chain.run(content=content[:5000])
            else:
                summary = content
            
            # Save to database if connection exists
            if self.db:
                self.db.insert_one({
                    'url': url,
                    'content': content[:10000],  # Limit stored content
                    'links': links[:20],  # Limit number of links
                    'summary': summary,
                    'timestamp': datetime.utcnow()
                })
            
            return {
                'content': content[:5000],
                'summary': summary,
                'links': links[:20]
            }
            
        except Exception as e:
            print(f"Error scraping website: {e}")
            return {'error': str(e)}

def render_scraping_ui():
    """Render the web scraping UI in Streamlit"""
    st.title("Web Scraping and Summarization")
    
    url = st.text_input("Enter URL to scrape", placeholder="https://example.com")
    
    if st.button("Scrape Website"):
        with st.spinner("Scraping in progress..."):
            scraper = WebScraper()
            result = scraper.scrape_website(url)
            
            if 'error' in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success("Scraping completed!")
                
                # Display summary
                st.subheader("AI-Generated Summary")
                st.write(result['summary'])
                
                # Display content preview
                with st.expander("Content Preview"):
                    st.write(result['content'][:500] + "...")
                
                # Display links
                st.subheader("Extracted Links")
                for i, link in enumerate(result['links']):
                    if i < 10:  # Limit displayed links
                        st.write(f"[{link['text']}]({link['url']})")
                
                # Save to session state for sharing with chat
                st.session_state.scraping_context = result['summary']
                
                # Add button to discuss with AI
                if st.button("Discuss with AI Assistant"):
                    st.session_state.chat_context = f"Scraped content: {result['summary']}"
                    st.session_state.nav_option = "Chat Assistant"
                    st.experimental_rerun()
