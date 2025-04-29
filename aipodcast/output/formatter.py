import json
import os
import datetime
from typing import Dict, Any, List

class OutputFormatter:
    """Formats and saves podcast conversations."""
    
    @staticmethod
    def save_as_json(conversation: List[Dict[str, str]], 
                    output_path: str = None,
                    metadata: Dict[str, Any] = None) -> str:
        """Save the conversation as a JSON file."""
        if output_path is None:
            # Use output directory at project root
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            output_dir = os.path.join(root_dir, "output")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"podcast_{timestamp}.json")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        output = {
            "metadata": metadata or {},
            "created_at": datetime.datetime.now().isoformat(),
            "conversation": conversation
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        return output_path
    
    @staticmethod
    def save_as_markdown(conversation: List[Dict[str, str]], 
                        output_path: str = None,
                        metadata: Dict[str, Any] = None) -> str:
        """Save the conversation as a Markdown file."""
        if output_path is None:
            # Use output directory at project root
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            output_dir = os.path.join(root_dir, "output")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"podcast_{timestamp}.md")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write metadata
            if metadata:
                f.write("# AI-Generated Podcast\n\n")
                f.write("## Metadata\n\n")
                for key, value in metadata.items():
                    f.write(f"- **{key}:** {value}\n")
                f.write(f"- **Created At:** {datetime.datetime.now().isoformat()}\n\n")
            
            # Write conversation
            f.write("## Conversation\n\n")
            for entry in conversation:
                speaker = entry.get('speaker', 'Unknown')
                text = entry.get('text', '')
                f.write(f"### {speaker}\n\n{text}\n\n")
                
        return output_path
    
    @staticmethod
    def save_conversation(conversation: List[Dict[str, str]], 
                        format_type: str = "markdown",
                        output_path: str = None,
                        metadata: Dict[str, Any] = None) -> str:
        """Save the conversation in the specified format."""
        if format_type.lower() == "json":
            return OutputFormatter.save_as_json(conversation, output_path, metadata)
        else:
            return OutputFormatter.save_as_markdown(conversation, output_path, metadata)
