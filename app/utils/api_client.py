"""
Perplexity API client utility for MCLG-WS project.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from app.config.settings import PERPLEXITY_API_KEY, PERPLEXITY_BASE_URL, PERPLEXITY_MODELS
import requests

class PerplexityClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PerplexityClient, cls).__new__(cls)
            cls._instance.initialize_client()
        return cls._instance
    
    def initialize_client(self):
        """Initialize the Perplexity API client."""
        try:
            # Ensure environment variables are loaded
            load_dotenv()
            
            if not PERPLEXITY_API_KEY:
                raise ValueError("PERPLEXITY_API_KEY missing in environment variables")
                
            if not PERPLEXITY_BASE_URL:
                raise ValueError("PERPLEXITY_BASE_URL not configured")

            self.client = OpenAI(
                api_key=PERPLEXITY_API_KEY,
                base_url=PERPLEXITY_BASE_URL
            )
            
            # Verify API connectivity
            test_response = self.client.chat.completions.create(
                model="sonar-pro",
                messages=[{"role": "user", "content": "connection test"}],
                max_tokens=1
            )
            
            if not test_response.choices:
                raise ConnectionError("Received empty response from API")

            self.models = PERPLEXITY_MODELS
            print("Perplexity API client initialized successfully")
            
        except Exception as e:
            self.client = None
            raise RuntimeError(f"API initialization failed: {str(e)}")
    
    def get_client(self):
        """Return the OpenAI client configured for Perplexity API."""
        if not self.client:
            raise ConnectionError("Perplexity API client not initialized")
        return self.client
    
    def get_model(self, purpose):
        """Get the appropriate model name for the given purpose."""
        if purpose not in self.models:
            raise ValueError(f"Unknown purpose: {purpose}")
        return self.models[purpose]
    
    def generate_completion(self, model, messages, temperature=0.7, max_tokens=2000):
        """Generate a chat completion using Perplexity API."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            print(f"Error generating completion: {e}")
            return {"error": str(e)}
        
    def generate_completion_via_requests(self, model, messages, temperature=0.7, max_tokens=2000):
        """Generate a chat completion using Perplexity API via requests."""
        try:
            headers = {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            response = requests.post(
                f"{PERPLEXITY_BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 401:
                return {"error": "Perplexity API authentication failed. Check your API key."}
            
            response_data = response.json()
            
            if "choices" not in response_data or not response_data["choices"]:
                raise ValueError("Invalid response structure: 'choices' missing or empty")
            
            return {
                "content": response_data["choices"][0]["message"]["content"],
                "model": response_data["model"],
                "usage": {
                    "prompt_tokens": response_data["usage"]["prompt_tokens"],
                    "completion_tokens": response_data["usage"]["completion_tokens"],
                    "total_tokens": response_data["usage"]["total_tokens"]
                }
            }
        except Exception as e:
            return {"error": str(e)}
