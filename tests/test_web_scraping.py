import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.web_scraping import WebScraper

class TestWebScraping(unittest.TestCase):
    @patch('app.web_scraping.requests.get')
    @patch('app.web_scraping.BeautifulSoup')
    @patch('app.web_scraping.LLMChain')
    def test_scrape_website(self, mock_llm_chain, mock_bs, mock_requests_get):
        # Setup mocks
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Test content</p><a href='https://example.com'>Link</a></body></html>"
        mock_requests_get.return_value = mock_response
        
        mock_soup = MagicMock()
        mock_body = MagicMock()
        mock_body.get_text.return_value = "Test content"
        mock_soup.find.return_value = mock_body
        
        mock_link = MagicMock()
        mock_link.__getitem__.return_value = "https://example.com"
        mock_link.get_text.return_value = "Link"
        mock_soup.find_all.return_value = [mock_link]
        
        mock_bs.return_value = mock_soup
        
        mock_chain = MagicMock()
        mock_chain.run.return_value = "Summary of test content"
        mock_llm_chain.return_value = mock_chain
        
        # Create WebScraper instance
        scraper = WebScraper()
        
        # Mock the database insertion
        scraper.db = MagicMock()
        
        # Call the scrape_website method
        result = scraper.scrape_website("https://example.com")
        
        # Assertions
        self.assertIn("summary", result)
        self.assertEqual(result["summary"], "Summary of test content")
        self.assertIn("links", result)
        
        # Verify requests.get was called with the correct URL
        mock_requests_get.assert_called_once_with(
            "https://example.com", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )

if __name__ == '__main__':
    unittest.main()
