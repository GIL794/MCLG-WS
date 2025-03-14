"""
Perplexity API client utility for MCLG-WS project.
"""
import os
from openai import OpenAI
from app.config.settings import PERPLEXITY_API_KEY, PERPLEXITY_BASE_URL, PERPLEXITY_MODELS

class PerplexityClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PerplexityClient, cls).__new__(cls)
            cls._instance.initialize_client()
        return cls._instance
    
    def initialize_client(self):
        """Initialize the Perplexity API client using OpenAI's compatible client."""
        try:
            if not PERPLEXITY_API_KEY:
                raise ValueError("Perplexity API key is not set in environment variables")
            
            # Create OpenAI client configured for Perplexity
            self.client = OpenAI(
                api_key=PERPLEXITY_API_KEY,
                base_url=PERPLEXITY_BASE_URL
            )
            
            # Test connection by listing models
            self.client.models.list()
            print("Successfully connected to Perplexity API")
            
            # Store model configurations
            self.models = PERPLEXITY_MODELS
            
        except Exception as e:
            print(f"Error initializing Perplexity API client: {e}")
            self.client = None
    
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
