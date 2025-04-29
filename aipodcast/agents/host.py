from typing import Dict, Any, List
from .agent import Agent
from ..models.ollama_client import OllamaClient

class HostAgent(Agent):
    """Host agent for the podcast."""
    
    def __init__(self, 
                name: str, 
                personality: str, 
                ollama_client: OllamaClient,
                language: str = "Hindi"):
        """Initialize the host agent."""
        super().__init__(name, personality, ollama_client, language)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the host."""
        base_prompt = super().get_system_prompt()
        host_specific = (
            "As a podcast host, you should ask engaging questions, follow up on interesting points, "
            "and guide the conversation naturally. Be respectful but not afraid to dig deeper into topics. "
            "Keep your questions concise and clear."
        )
        return f"{base_prompt}\n\n{host_specific}"
    
    def generate_response(self, 
                         conversation_history: List[Dict[str, str]], 
                         current_topic: str, 
                         tone: str,
                         max_tokens: int = 200) -> str:
        """Generate a host response or question."""
        history_text = self.format_history(conversation_history)
        
        # Determine if this is the start of the podcast
        is_start = len(conversation_history) < 2
        
        if is_start:
            prompt = (
                f"आप {self.name} हैं और एक पॉडकास्ट की शुरुआत कर रहे हैं। "
                f"विषय है: {current_topic}। "
                f"टोन है: {tone}। "
                f"पॉडकास्ट की शुरुआत करें और अपने अतिथि {conversation_history[0]['speaker'] if conversation_history else 'अतिथि'} "
                f"का स्वागत करें, फिर एक प्रासंगिक प्रश्न पूछें।"
            )
        else:
            prompt = (
                f"आप {self.name} हैं और एक पॉडकास्ट होस्ट हैं। "
                f"अब तक की बातचीत:\n\n{history_text}\n\n"
                f"विषय है: {current_topic}। टोन है: {tone}। "
                f"पिछले जवाब पर फॉलो-अप करते हुए या विषय को आगे बढ़ाते हुए एक नया प्रश्न या टिप्पणी दें।"
            )
        
        response = self.ollama_client.generate(
            prompt=prompt,
            system_prompt=self.get_system_prompt(),
            max_tokens=max_tokens
        )
        
        # Ensure the response is in Hindi
        if not self.ollama_client.is_hindi(response):
            response = self.ollama_client.translate_to_hindi(response)
            
        return response
