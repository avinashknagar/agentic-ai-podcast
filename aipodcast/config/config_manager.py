import os
import yaml
import glob
from typing import Dict, Any

class ConfigManager:
    """Manages loading and validating podcast configurations."""
    
    def __init__(self, config_path: str = None):
        """Initialize with optional path to config file."""
        self.default_config_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
        self.config_path = config_path
        self.config = self._load_config()
        
    def _get_latest_input_config(self) -> str:
        """Find the latest YAML file in the inputs folder."""
        # Get project root directory (2 levels up from this file)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        inputs_dir = os.path.join(root_dir, "inputs")
        
        if not os.path.exists(inputs_dir):
            return None
            
        # Get all YAML files in the inputs directory
        yaml_files = glob.glob(os.path.join(inputs_dir, "*.yaml"))
        yaml_files += glob.glob(os.path.join(inputs_dir, "*.yml"))
        
        if not yaml_files:
            return None
            
        # Return the most recently modified file
        return max(yaml_files, key=os.path.getmtime)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        # Priority: 1. Explicitly provided config path, 2. Latest file from inputs, 3. Default config
        config_path = self.config_path
        
        if not (config_path and os.path.exists(config_path)):
            latest_input = self._get_latest_input_config()
            if latest_input:
                config_path = latest_input
                print(f"Using latest config from inputs folder: {os.path.basename(config_path)}")
            else:
                config_path = self.default_config_path
                print(f"No config specified or found in inputs folder. Using default config.")
        
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            
        # Validate the loaded config
        self._validate_config(config)
        return config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Ensure all required configuration fields are present."""
        required_fields = {
            'podcast_config': [
                'host', 'guest', 'language', 'tone', 'theme',
                'max_tokens_per_response', 'total_podcast_duration_minutes',
                'ollama_model'
            ]
        }
        
        pc = config.get('podcast_config', {})
        for field in required_fields['podcast_config']:
            if field not in pc:
                raise ValueError(f"Missing required configuration field: podcast_config.{field}")
                
        # Validate host and guest have required fields
        for agent_type in ['host', 'guest']:
            agent = pc.get(agent_type, {})
            if not isinstance(agent, dict) or 'name' not in agent or 'personality' not in agent:
                raise ValueError(f"Invalid {agent_type} configuration. Must include name and personality.")
    
    def get_config(self) -> Dict[str, Any]:
        """Return the loaded configuration."""
        return self.config
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update the current configuration."""
        self.config.update(new_config)
        self._validate_config(self.config)
