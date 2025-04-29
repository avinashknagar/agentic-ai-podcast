# AI Podcast Generator - Project Structure

```
aipodcast/
│
├── config/
│   ├── __init__.py
│   ├── config_manager.py       # Handles configuration loading/validation
│   └── default_config.yaml     # Default podcast configuration
│
├── agents/
│   ├── __init__.py
│   ├── agent.py                # Base agent class
│   ├── host.py                 # Host agent implementation
│   └── guest.py                # Guest agent implementation
│
├── conversation/
│   ├── __init__.py
│   ├── manager.py              # Controls conversation flow
│   ├── memory.py               # Maintains conversation history
│   └── validator.py            # Validates Hindi language output
│
├── models/
│   ├── __init__.py
│   └── ollama_client.py        # Interface with Ollama models
│
├── templates/
│   ├── __init__.py
│   └── prompts.py              # Prompt templates for different contexts
│
├── output/
│   ├── __init__.py
│   └── formatter.py            # Output to JSON/Markdown
│
├── cli/
│   ├── __init__.py
│   └── interface.py            # Command line interface
│
├── main.py                     # Main entry point
├── setup.py                    # For packaging
└── README.md                   # Project documentation
```
