import argparse
import os
import yaml
import sys
import datetime
from typing import Dict, Any

from ..config import ConfigManager
from ..models import OllamaClient
from ..agents import HostAgent, GuestAgent
from ..conversation import ConversationManager
from ..output import OutputFormatter

class CLI:
    """Command-line interface for the AI podcast generator."""
    
    def __init__(self):
        """Initialize the CLI parser."""
        self.parser = self._create_parser()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(description='AI Podcast Generator')
        
        parser.add_argument('--config', '-c', type=str,
                          help='Path to a custom configuration YAML file')
        
        parser.add_argument('--output', '-o', type=str,
                          help='Output file path for the generated podcast')
        
        parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='json',
                          help='Output format (default: json)')
        
        parser.add_argument('--host', type=str,
                          help='Name of the host character')
        
        parser.add_argument('--guest', type=str,
                          help='Name of the guest character')
        
        parser.add_argument('--theme', type=str,
                          help='Theme or topic of the podcast')
        
        parser.add_argument('--tone', type=str,
                          help='Tone of the conversation')
        
        parser.add_argument('--duration', type=int,
                          help='Duration of the podcast in minutes')
        
        parser.add_argument('--model', type=str,
                          help='Ollama model to use')
        
        return parser
    
    def parse_args(self):
        """Parse command-line arguments."""
        return self.parser.parse_args()
    
    def run(self):
        """Run the podcast generator with the provided arguments."""
        args = self.parse_args()
        
        # Load the config
        config_manager = ConfigManager(args.config)
        config = config_manager.get_config()
        
        # Override config with command-line arguments
        podcast_config = config['podcast_config']
        
        if args.host:
            podcast_config['host']['name'] = args.host
            
        if args.guest:
            podcast_config['guest']['name'] = args.guest
            
        if args.theme:
            podcast_config['theme'] = args.theme
            
        if args.tone:
            podcast_config['tone'] = args.tone
            
        if args.duration:
            podcast_config['total_podcast_duration_minutes'] = args.duration
            
        if args.model:
            podcast_config['ollama_model'] = args.model
            
        if args.format:
            podcast_config['output_format'] = args.format
            
        if args.output:
            podcast_config['output_file'] = args.output
        else:
            # If no output file specified, use default in output directory
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_root = os.path.dirname(root_dir)
            output_dir = os.path.join(project_root, "output")
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            podcast_config['output_file'] = os.path.join(output_dir, f"podcast_{timestamp}.{podcast_config['output_format']}")
        
        # Initialize the Ollama client
        ollama_client = OllamaClient(model=podcast_config['ollama_model'])
        
        # Check if Ollama is running
        try:
            print("Checking connection to Ollama...")
            test_response = ollama_client.generate("Hello", max_tokens=5)
            print("Connected to Ollama successfully!")
        except Exception as e:
            print(f"Error: Could not connect to Ollama. Make sure it's running on localhost:11434")
            print(f"Error details: {str(e)}")
            sys.exit(1)
        
        # Initialize the agents
        host = HostAgent(
            name=podcast_config['host']['name'],
            personality=podcast_config['host']['personality'],
            ollama_client=ollama_client,
            language=podcast_config['language']
        )
        
        guest = GuestAgent(
            name=podcast_config['guest']['name'],
            personality=podcast_config['guest']['personality'],
            ollama_client=ollama_client,
            language=podcast_config['language']
        )
        
        # Initialize the conversation manager
        conversation_manager = ConversationManager(
            host=host,
            guest=guest,
            theme=podcast_config['theme'],
            tone=podcast_config['tone'],
            max_tokens_per_response=podcast_config['max_tokens_per_response'],
            total_podcast_duration_minutes=podcast_config['total_podcast_duration_minutes']
        )
        
        # Generate the conversation
        print(f"Generating podcast between {host.name} and {guest.name}...")
        print(f"Theme: {podcast_config['theme']}")
        print(f"Tone: {podcast_config['tone']}")
        print(f"Duration: {podcast_config['total_podcast_duration_minutes']} minutes")
        print(f"Model: {podcast_config['ollama_model']}")
        print("-" * 50)
        
        conversation = conversation_manager.start_conversation()
        
        # Save the conversation
        metadata = {
            "host": podcast_config['host']['name'],
            "guest": podcast_config['guest']['name'],
            "theme": podcast_config['theme'],
            "tone": podcast_config['tone'],
            "language": podcast_config['language'],
            "duration": f"{podcast_config['total_podcast_duration_minutes']} minutes",
            "model": podcast_config['ollama_model']
        }
        
        output_path = podcast_config.get('output_file')
        output_format = podcast_config.get('output_format', 'json')
        
        saved_path = OutputFormatter.save_conversation(
            conversation, 
            format_type=output_format, 
            output_path=output_path,
            metadata=metadata
        )
        
        print("-" * 50)
        print(f"Podcast generated and saved to: {saved_path}")
        
        return saved_path
