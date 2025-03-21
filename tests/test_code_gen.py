"""
Idea founded by Gabriele Iacopo Langellotto

Unit tests for the code generation module.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.code_generation import CodeGenerator

class TestCodeGeneration(unittest.TestCase):
    @patch('app.code_generation.OpenAI')
    @patch('app.code_generation.LLMChain')
    def test_generate_code(self, mock_llm_chain, mock_openai):
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.run.return_value = "def hello_world():\n    print('Hello, World!')"
        mock_llm_chain.return_value = mock_chain
        
        # Create CodeGenerator instance with mocked dependencies
        code_gen = CodeGenerator()
        
        # Call the generate_code method
        result = code_gen.generate_code(
            project_context="Test project",
            existing_code="",
            task="Write a hello world function"
        )
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertIn("def hello_world", result)
        
        # Verify that the LLMChain's run method was called with the expected parameters
        mock_chain.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
