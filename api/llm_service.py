import os
import time
import logging
from typing import Dict, Any
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5 model for wider availability
        self._client = None
        
    @property
    def client(self):
        if self._client is None:
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
            self._client = OpenAI(api_key=api_key)
        return self._client
        
    def process_query(self, query: str, quantum_prompt: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Process a query through the OpenAI API and return the response with quantum analysis.
        
        Args:
            query: The user's original query
            quantum_prompt: The quantum analysis prompt to append
            max_retries: Maximum number of retry attempts for rate limits
            
        Returns:
            Dict containing the processed response
            
        Raises:
            ValueError: If there are API issues or rate limits
            RuntimeError: For unexpected errors
        """
        retry_count = 0
        base_delay = 1  # Base delay in seconds
        
        while retry_count <= max_retries:
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
                
            except openai.RateLimitError as e:
                retry_count += 1
                error_msg = str(e)
                
                # Check if it's a quota exceeded error
                if "insufficient_quota" in error_msg:
                    logger.error(f"API quota exceeded: {error_msg}")
                    raise ValueError("The API quota has been exceeded. Please try again later or contact support.")
                    
                # If it's a regular rate limit and we have retries left
                if retry_count <= max_retries:
                    delay = base_delay * (2 ** (retry_count - 1))  # Exponential backoff
                    logger.info(f"Rate limit hit, retrying in {delay} seconds (attempt {retry_count}/{max_retries})")
                    time.sleep(delay)
                else:
                    logger.error(f"Rate limit exceeded after {max_retries} retries: {error_msg}")
                    raise ValueError("API rate limit exceeded. Please try again in a few moments.")
                    
            except openai.APIError as e:
                logger.error(f"OpenAI API error: {str(e)}")
                raise ValueError("Temporary service interruption. Please try again in a few moments.")
                
            except openai.APIConnectionError as e:
                logger.error(f"OpenAI API connection error: {str(e)}")
                raise ValueError("Unable to connect to the service. Please check your internet connection and try again.")
                
            except Exception as e:
                logger.error(f"Error processing query through LLM: {str(e)}")
                if "model_not_found" in str(e):
                    raise ValueError("The selected AI model is currently unavailable. Please try again later.")
                raise ValueError(f"An unexpected error occurred: {str(e)}")

llm_service = LLMService()
