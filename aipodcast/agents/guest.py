from typing import Dict, Any, List
from .agent import Agent
from ..models.ollama_client import OllamaClient

class GuestAgent(Agent):
    """Guest agent for the podcast."""
    
    def __init__(self, 
                name: str, 
                personality: str, 
                ollama_client: OllamaClient,
                language: str = "Hindi"):
        """Initialize the guest agent."""
        super().__init__(name, personality, ollama_client, language)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the guest."""
        base_prompt = super().get_system_prompt()
        guest_specific = (
            "As a podcast guest, you should provide thoughtful and insightful responses. "
            "Share personal anecdotes, opinions, and expertise when appropriate. "
            "Your responses should reflect your character's knowledge, values, and speaking style."
        )
        return f"{base_prompt}\n\n{guest_specific}"
    
    def generate_response(self, 
                         conversation_history: List[Dict[str, str]], 
                         current_topic: str, 
                         tone: str,
                         max_tokens: int = 200) -> str:
        """Generate a guest response to the host's question."""
        history_text = self.format_history(conversation_history)
        
        if self.language.lower() == "hindi":
            prompt = (
                f"आप {self.name} हैं और एक पॉडकास्ट में अतिथि हैं। "
                f"अब तक की बातचीत:\n\n{history_text}\n\n"
                f"विषय है: {current_topic}। टोन है: {tone}। "
                f"होस्ट के पिछले प्रश्न या टिप्पणी का उत्तर दें। "
                f"अपने व्यक्तित्व और विशेषज्ञता के अनुसार जवाब दें।"
            )
        else:  # English or other languages
            prompt = (
                f"You are {self.name} and you're a guest on a podcast. "
                f"Conversation so far:\n\n{history_text}\n\n"
                f"The topic is: {current_topic}. The tone is: {tone}. "
                f"Answer the host's previous question or comment. "
                f"Respond according to your personality and expertise."
            )
        
        response = self.ollama_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            max_tokens=max_tokens
        )
        
        # Only check/translate if language is Hindi
        if self.language.lower() == "hindi" and not self.ollama_client.is_hindi(response):
            response = self.ollama_client.translate_to_hindi(response)
            
        return response
