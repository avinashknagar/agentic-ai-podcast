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
        language_instruction = ""
        if self.language.lower() == "hindi":
            language_instruction = "Always respond in Hindi using Devanagari script."
        elif self.language.lower() == "english":
            language_instruction = "Always respond in English."
        else:
            language_instruction = f"Always respond in {self.language}."
            
        return (
            f"You are {self.name}. "
            f"Your personality is: {self.personality}. "
            f"{language_instruction} "
            "Maintain your unique character traits and speaking style throughout the conversation. "
            "Draw upon the knowledge and experiences that align with your identity. "
            "Your responses should naturally reflect your character without explicitly stating your traits. "
            "Respond as if you genuinely embody this identity."
        )
        
    def generate_response(self, 
                         conversation_history: List[Dict[str, str]], 
                         current_topic: str, 
                         tone: str,
                         max_tokens: int = 200) -> str:
        """Generate a response based on conversation history and current topic."""
        system_prompt = self.get_system_prompt()
        formatted_history = self.format_history(conversation_history)
        
        user_prompt = (
            f"Topic: {current_topic}\n"
            f"Tone: {tone}\n\n"
            f"Previous conversation:\n{formatted_history}\n"
            f"Now, as {self.name}, respond to the conversation naturally, keeping in mind the current topic. "
            f"Your response should be in the style of your personality: {self.personality}."
        )
        
        response = self.ollama_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens
        )
        
        return response.strip()
    
    def format_history(self, conversation_history: List[Dict[str, str]]) -> str:
        """Format conversation history for the prompt."""
        formatted = ""
        for entry in conversation_history[-5:]:  # Only use the last 5 exchanges to avoid context length issues
            speaker = entry.get('speaker', '')
            text = entry.get('text', '')
            formatted += f"{speaker}: {text}\n\n"
        return formatted
