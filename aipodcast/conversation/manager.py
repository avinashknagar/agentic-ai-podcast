from typing import Dict, Any, List, Tuple
import time
import math
from ..agents.host import HostAgent
from ..agents.guest import GuestAgent
from ..models.ollama_client import OllamaClient

class ConversationManager:
    """Manages the podcast conversation flow."""
    
    def __init__(self, 
                host: HostAgent, 
                guest: GuestAgent, 
                theme: str,
                tone: str,
                max_tokens_per_response: int,
                total_podcast_duration_minutes: int):
        """Initialize the conversation manager."""
        self.host = host
        self.guest = guest
        self.theme = theme
        self.tone = tone
        self.max_tokens_per_response = max_tokens_per_response
        self.total_podcast_duration_minutes = total_podcast_duration_minutes
        self.conversation_history = []
        
        # Estimate the number of exchanges based on duration and token count
        # This is a rough estimate: assuming ~1.5 words per token and ~150 words per minute
        # For a back-and-forth (2 turns) in conversation
        words_per_minute = 150
        tokens_per_minute = words_per_minute / 1.5
        total_tokens = tokens_per_minute * total_podcast_duration_minutes
        self.estimated_exchanges = math.ceil(total_tokens / (max_tokens_per_response * 2))
    
    def start_conversation(self) -> List[Dict[str, str]]:
        """Start and manage the entire podcast conversation."""
        print(f"Starting podcast with {self.estimated_exchanges} estimated exchanges...")
        
        # Add initial context - will be empty but serves as a placeholder for the first turn
        self.conversation_history = []
        
        # Start with host introduction
        host_intro = self.host.generate_response(
            self.conversation_history,
            self.theme,
            self.tone,
            self.max_tokens_per_response
        )
        self.add_to_history(self.host.name, host_intro)
        print(f"{self.host.name}: {host_intro}\n")
        
        # Alternate between host and guest for the estimated number of exchanges
        for i in range(self.estimated_exchanges - 1):  # -1 because we already added the intro
            # Guest response
            guest_response = self.guest.generate_response(
                self.conversation_history,
                self.theme,
                self.tone,
                self.max_tokens_per_response
            )
            self.add_to_history(self.guest.name, guest_response)
            print(f"{self.guest.name}: {guest_response}\n")
            
            # Host question/comment (except for the last exchange)
            if i < self.estimated_exchanges - 2:
                host_response = self.host.generate_response(
                    self.conversation_history,
                    self.theme,
                    self.tone,
                    self.max_tokens_per_response
                )
                self.add_to_history(self.host.name, host_response)
                print(f"{self.host.name}: {host_response}\n")
        
        # Add host closing
        host_closing = self.generate_closing()
        self.add_to_history(self.host.name, host_closing)
        print(f"{self.host.name}: {host_closing}\n")
        
        return self.conversation_history
    
    def generate_closing(self) -> str:
        """Generate a closing statement from the host."""
        prompt = (
            f"आप {self.host.name} हैं और अपने पॉडकास्ट को समाप्त कर रहे हैं। "
            f"अतिथि {self.guest.name} को धन्यवाद दें और श्रोताओं से विदा लें। "
            f"पॉडकास्ट के मुख्य बिंदुओं का संक्षिप्त सारांश दें।"
        )
        
        closing = self.host.ollama_client.generate(
            prompt=prompt,
            system_prompt=self.host.get_system_prompt(),
            max_tokens=self.max_tokens_per_response
        )
        
        # Ensure the closing is in Hindi
        if not self.host.ollama_client.is_hindi(closing):
            closing = self.host.ollama_client.translate_to_hindi(closing)
            
        return closing
    
    def add_to_history(self, speaker: str, text: str) -> None:
        """Add an exchange to the conversation history."""
        self.conversation_history.append({
            'speaker': speaker,
            'text': text,
            'timestamp': time.time()
        })
