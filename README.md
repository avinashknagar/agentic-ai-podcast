# AI Podcast Generator

An AI-powered podcast generator that simulates conversations between historical or fictional characters in Hindi.

## Features

- Generate podcasts using local Ollama models (no external APIs)
- Simulate conversations between a host and guest in Hindi
- Configurable personalities, themes, tones, and podcast length
- Export conversations in Markdown or JSON format
- Command-line interface for easy usage

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- At least one LLM model pulled in Ollama (e.g., `llama3`, `mistral`)

## Installation

Clone the repository and install the package:

```bash
git clone /path/to/repo
cd podcast
pip install -e .
```

## Usage

### Basic Usage

Run with default settings:

```bash
python main.py
```

This will automatically use the most recent YAML configuration file from the `inputs/` folder. If no files exist there, it will use the default configuration.

### Custom Configuration

Use a custom configuration file:

```bash
python main.py --config my_config.yaml
```

### Command-line Options

Override specific settings:

```bash
python main.py --host "Rabindranath Tagore" --guest "Lata Mangeshkar" --theme "Music and Poetry" --tone "Philosophical" --duration 15 --model "mistral" --format json --output "podcast_output.json"
```

## Configuration

Place your YAML configuration files in the `inputs/` folder. The system will automatically use the most recently modified file when you run without specifying a config file.

Create a YAML file with the following structure:

```yaml
podcast_config:
  host:
    name: "Character Name"
    personality: "Description of personality traits"
  guest:
    name: "Character Name" 
    personality: "Description of personality traits"
  language: "Hindi"
  tone: "Formal/Inspirational/Humorous/Philosophical"
  theme: "Topic of conversation"
  max_tokens_per_response: 200
  total_podcast_duration_minutes: 10
  ollama_model: "llama3"
  output_format: "markdown"
  output_file: "podcast_output.md"
```

## Example Output

The generated conversation will be saved in either Markdown or JSON format, depending on your configuration.

## License

Open source under the MIT License

## Author

Avinash
