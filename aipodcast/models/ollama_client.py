import requests
import json
from typing import Dict, Any, Optional, List

class OllamaClient:
    """Client for interacting with Ollama local models."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        """Initialize the Ollama client with base URL and model."""
        self.base_url = base_url
        self.model = model
        self.api_generate = f"{self.base_url}/api/generate"
        
    def set_model(self, model: str) -> None:
        """Update the model being used."""
        self.model = model
        
    def generate(self, 
                prompt: str, 
                system_prompt: Optional[str] = None,
                max_tokens: int = 200) -> str:
        """Generate text using the specified Ollama model."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "max_tokens": max_tokens
            }
            
            if system_prompt:
                payload["system"] = system_prompt
                
            response = requests.post(self.api_generate, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Error from Ollama API: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error communicating with Ollama: {str(e)}")
            return ""
    
    def is_hindi(self, text: str, min_hindi_ratio: float = 0.7) -> bool:
        """
        Check if text is primarily Hindi (uses a simple heuristic).
        Returns True if the text contains at least min_hindi_ratio of Devanagari script.
        """
        if not text:
            return False
            
        # Unicode range for Devanagari script used in Hindi
        hindi_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        total_chars = sum(1 for char in text if not char.isspace())
        
        if total_chars == 0:
            return False
            
        hindi_ratio = hindi_chars / total_chars
        return hindi_ratio >= min_hindi_ratio
    
    def translate_to_hindi(self, text: str) -> str:
        """Translate text to Hindi using the model."""
        prompt = f"Translate the following text to Hindi (use Devanagari script): {text}"
        return self.generate(prompt, system_prompt="You are a helpful translator that translates text to Hindi.")
