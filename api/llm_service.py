import os
import logging
from typing import Dict, Any
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # Using more widely available model
        self._client = None
        
    @property
    def client(self):
        if self._client is None:
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
            self._client = OpenAI(api_key=api_key)
        return self._client
        
    def process_query(self, query: str, quantum_prompt: str) -> Dict[str, Any]:
        """
        Process a query through the OpenAI API and return the response with quantum analysis.
        
        Args:
            query: The user's original query
            quantum_prompt: The quantum analysis prompt to append
            
        Returns:
            Dict containing the processed response
        """
        try:
            # Combine the query with the quantum prompt
            full_prompt = f"{query}\n\n{quantum_prompt}"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a quantum state analyzer that analyzes text and provides detailed quantum state analysis."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            
            return {
                "original_query": query,
                "full_response": response_text
            }
            
        except Exception as e:
            logger.error(f"Error processing query through LLM: {str(e)}")
            raise RuntimeError(f"Failed to process query: {str(e)}")

llm_service = LLMService()
