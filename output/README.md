# Output Directory

This directory contains generated podcast conversations in JSON or Markdown format.

Files are named with a timestamp pattern: `podcast_YYYYMMDD_HHMMSS.json` or `podcast_YYYYMMDD_HHMMSS.md`

## JSON Format

The JSON output contains:

```json
{
  "metadata": {
    "host": "Host Name",
    "guest": "Guest Name",
    "theme": "Conversation Theme",
    "tone": "Conversation Tone",
    "language": "Hindi",
    "duration": "X minutes",
    "model": "ollama model used"
  },
  "created_at": "ISO datetime",
  "conversation": [
    {
      "speaker": "Speaker Name",
      "text": "Speaker's dialogue text",
      "timestamp": 1234567890.123
    },
    ...
  ]
}
```

You can parse this JSON file for further processing or text-to-speech conversion.
