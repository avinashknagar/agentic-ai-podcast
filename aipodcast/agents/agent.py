from typing import Dict, Any, List
from ..models.ollama_client import OllamaClient

class Agent:
    """Base class for podcast agents (host and guest)."""
    
    def __init__(self, 
                name: str, 
                personality: str, 
                ollama_client: OllamaClient,
                language: str = "Hindi"):
        """Initialize an agent with name and personality."""
        self.name = name
        self.personality = personality
        self.ollama_client = ollama_client
        self.language = language
        
    def get_system_prompt(self) -> str:
        """Get the basic system prompt for this agent."""
        return (
            f"You are {self.name}. "
            f"Your personality is: {self.personality}. "
            f"Always respond in {self.language} using Devanagari script. "
            "Maintain your unique character traits and speaking style throughout the conversation."
        )
        
    def generate_response(self, 
                         conversation_history: List[Dict[str, str]], 
                         current_topic: str, 
                         tone: str,
                         max_tokens: int = 200) -> str:
        """Generate a response based on conversation history and current topic."""
        # This is implemented in the subclasses
        raise NotImplementedError("Subclasses must implement this method")
    
    def format_history(self, conversation_history: List[Dict[str, str]]) -> str:
        """Format conversation history for the prompt."""
        formatted = ""
        for entry in conversation_history[-5:]:  # Only use the last 5 exchanges to avoid context length issues
            speaker = entry.get('speaker', '')
            text = entry.get('text', '')
            formatted += f"{speaker}: {text}\n\n"
        return formatted
