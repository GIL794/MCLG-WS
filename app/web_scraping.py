"""
Web scraping module using Perplexity API with sonar-deep-research.
"""
import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from app.utils.api_client import PerplexityClient
from app.utils.db_connection import DatabaseManager
from app.config.settings import COLLECTIONS

class WebScraper:
    def __init__(self):
        # Initialize Perplexity client
        perplexity = PerplexityClient()
        self.client = perplexity.get_client()
        self.model = perplexity.get_model("web")  # sonar-deep-research
        
        # Get database collection
        db_manager = DatabaseManager()
        self.db = db_manager.get_collection(COLLECTIONS["scraping"])


    def extract_citations(self, text):
        """Extract citation information from the response text."""
        citations = []
        # Basic regex pattern to find citations in the format $$number$$
        citation_pattern = r'$$(\d+)$$'
        matches = re.findall(citation_pattern, text)
        
        # Create unique citation list
        unique_citations = list(set(matches))
        
        for citation in unique_citations:
            # Look for citation details (often at the end of the text)
            citation_detail_pattern = r'$$' + citation + r'$$(.*?)(?:$$\d+$$|$)'
            detail_matches = re.findall(citation_detail_pattern, text, re.DOTALL)
            
            if detail_matches:
                citations.append({
                    "number": citation,
                    "details": detail_matches.strip()
                })
            else:
                citations.append({
                    "number": citation,
                    "details": "Citation details not found"
                })
        
        return citations
    
    def scrape_website(self, url):
        """Scrape website using sonar-deep-research capabilities."""
        try:
            # First, attempt to validate the URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            page_response = requests.get(url, headers=headers, timeout=10)
            if page_response.status_code == 401:
                return {"error": "Authorization required. This website does not allow anonymous scraping."}
            
            # Construct prompt for web scraping using sonar-deep-research
            messages = [
                {"role": "system", "content": "You are a professional web researcher who provides comprehensive and factual information from websites."},
                {"role": "user", "content": f"""
                Please conduct deep research on the content from the website: {url}
                
                Provide a comprehensive research report covering:
                1. A summary of the main content and purpose of the website
                2. Key topics, themes, and information presented
                3. Important data points, statistics, or facts
                4. Sources cited on the page (if any)
                5. Overall credibility assessment of the information
                
                Include appropriate citations for any information you provide.
                Organize your response with clear headings and structure.
                """}
            ]
            
            # Get response from Perplexity
            perplexity = PerplexityClient()
            response = perplexity.generate_completion(
                model=self.model,  # sonar-deep-research
                messages=messages,
                temperature=0.3,   # Lower temperature for factual reporting
                max_tokens=4000    # Allow for comprehensive research
            )
            
            if "error" in response:
                return {"error": response["error"]}
            
            content = response["content"]
            
            # Extract citations
            citations = self.extract_citations(content)
            
            # Also get basic metadata from the URL for reference
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                page_response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(page_response.text, 'html.parser')
                
                title = soup.title.string if soup.title else "No title found"
                meta_description = ""
                description_tag = soup.find("meta", {"name": "description"})
                if description_tag:
                    meta_description = description_tag.get("content", "")
                
                # Extract links for reference
                links = []
                for link in soup.find_all('a', href=True)[:20]:  # Limit to 20 links
                    href = link['href']
                    if href.startswith('http'):
                        links.append({
                            'url': href,
                            'text': link.get_text(strip=True)
                        })
            except Exception as e:
                print(f"Error scraping website: {e}")
                return {"error": str(e)}
            
            # Prepare result with Perplexity's research and basic metadata
            result = {
                'url': url,
                'title': title,
                'meta_description': meta_description,
                'ai_research': content,
                'citations': citations,
                'links': links,
                'model': response["model"],
                'token_usage': response["usage"],
                'timestamp': datetime.utcnow()
            }
            
            # Save to database if connection exists
            if self.db is not None:
                self.db.insert_one(result)
            
            return result
            
        except Exception as e:
            print(f"Error scraping website: {e}")
            return {"error": str(e)}

def render_scraping_ui():
    """Render the web scraping UI in Streamlit."""
    st.title("AI Web Research")
    
    url = st.text_input("Enter URL to research", placeholder="https://example.com")
    
    if st.button("Research Website"):
        if not url:
            st.error("Please enter a URL")
            return
            
        with st.spinner("Researching website content... This may take a minute."):
            scraper = WebScraper()
            result = scraper.scrape_website(url)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success("Research completed!")
                
                # Display basic metadata
                st.subheader(f"Research Results: {result['title']}")
                
                # Display AI research
                st.markdown(result['ai_research'])
                
                # Display citations if available
                if result['citations']:
                    with st.expander("Citations"):
                        for citation in result['citations']:
                            st.write(f"[{citation['number']}] {citation['details']}")
                
                # Display extracted links
                with st.expander("Extracted Links"):
                    for link in result['links']:
                        st.write(f"[{link['text']}]({link['url']})")
                
                # Token usage information
                with st.expander("API Usage Information"):
                    st.write(f"Model used: {result['model']}")
                    st.write(f"Token usage: {result['token_usage']}")
                
                # Save to session state for sharing with chat
                st.session_state.scraping_context = result['ai_research'][:1000]  # Limit length
                
                # Add button to discuss with AI
                if st.button("Discuss with AI Assistant"):
                    st.session_state.chat_context = f"Web research content: {result['ai_research'][:1000]}"
                    st.session_state.nav_option = "Chat Assistant"
                    st.experimental_rerun()
