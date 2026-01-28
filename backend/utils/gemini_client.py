"""
Gemini Client - Wrapper for Google Gemini API calls
Handles authentication and request formatting
"""

import os
import google.generativeai as genai
from typing import Optional


class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with API key from environment"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please add it to your .env file"
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Try different model names to find one that works
        # Updated for Gemini 2.x/3.x models (as of 2025)
        model_options = [
            'models/gemini-2.5-flash',      # Fast and stable (recommended)
            'models/gemini-flash-latest',   # Always points to latest flash
            'models/gemini-2.0-flash',      # Fallback to 2.0
            'models/gemini-pro-latest',     # Latest pro model
            'models/gemini-2.5-pro',        # More powerful if needed
        ]
        
        self.model = None
        self.model_name = None
        
        # Try to initialize a model without testing (to avoid rate limits on startup)
        for model_name in model_options:
            try:
                self.model = genai.GenerativeModel(model_name)
                self.model_name = model_name
                print(f"✓ Gemini Client initialized with model: {self.model_name}")
                break
            except Exception as e:
                print(f"  Trying {model_name}... failed: {str(e)[:80]}")
                continue
        
        if not self.model:
            # Fallback to most common model
            try:
                self.model_name = 'models/gemini-2.5-flash'
                self.model = genai.GenerativeModel(self.model_name)
                print(f"✓ Gemini Client initialized with model: {self.model_name} (fallback)")
            except Exception as e:
                raise ValueError(
                    "Could not initialize Gemini model. "
                    "Please check your API key and internet connection."
                )
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 1500,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 40,
        max_retries: int = 3
    ) -> str:
        """
        Generate a response using Gemini API with retry logic
        
        Args:
            prompt (str): The input prompt for generation
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Controls randomness (0.0-1.0)
            top_p (float): Nucleus sampling parameter
            top_k (int): Top-k sampling parameter
            max_retries (int): Maximum number of retry attempts
        
        Returns:
            str: Generated text response
        """
        import time
        import re
        
        for attempt in range(max_retries):
            try:
                # Configure generation parameters
                generation_config = genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                )
                
                # Generate response
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                # Extract text from response
                if response and response.text:
                    return response.text.strip()
                else:
                    return "Error: No response generated"
            
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error (429)
                if "429" in error_str or "quota" in error_str.lower():
                    # Extract retry delay from error message
                    retry_match = re.search(r'retry in (\d+\.?\d*)', error_str)
                    if retry_match:
                        retry_seconds = float(retry_match.group(1))
                        print(f"⚠️  Rate limit hit. Waiting {retry_seconds:.1f}s before retry {attempt + 1}/{max_retries}...")
                        time.sleep(retry_seconds + 1)  # Add 1 second buffer
                        continue
                    else:
                        # Default wait time for rate limits
                        wait_time = 20 * (attempt + 1)  # Exponential backoff
                        print(f"⚠️  Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                        time.sleep(wait_time)
                        continue
                else:
                    # Not a rate limit error, raise immediately
                    error_msg = f"Gemini API Error: {error_str}"
                    print(f"❌ {error_msg}")
                    raise Exception(error_msg)
        
        # If we exhausted all retries
        raise Exception(
            "Rate limit exceeded. Please wait a minute and try again. "
            "Free tier limit: 5 requests per minute. "
            "Consider upgrading your API plan for higher limits."
        )
    
    def generate_with_safety(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> dict:
        """
        Generate response with safety ratings included
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Temperature setting
        
        Returns:
            dict: Response with text and safety ratings
        """
        try:
            generation_config = genai.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return {
                'text': response.text.strip() if response.text else '',
                'safety_ratings': response.safety_ratings if hasattr(response, 'safety_ratings') else [],
                'finish_reason': response.candidates[0].finish_reason if response.candidates else None
            }
        
        except Exception as e:
            return {
                'text': '',
                'error': str(e),
                'safety_ratings': [],
                'finish_reason': None
            }
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string
        
        Args:
            text (str): Input text
        
        Returns:
            int: Approximate token count
        """
        try:
            result = self.model.count_tokens(text)
            return result.total_tokens
        except Exception as e:
            print(f"Warning: Could not count tokens: {e}")
            # Rough approximation: 1 token ≈ 4 characters
            return len(text) // 4
    
    def __str__(self):
        return f"GeminiClient(model={self.model_name})"