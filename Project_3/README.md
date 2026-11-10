# Project 3: Multi-Provider Chatbot

CLI chatbot that switches between Gemini and OpenRouter mid-chat.

## Run
```
python multi_provider.py
```

## Commands
- `/models`: pick a provider and model
- `quit`: exit and show token and cost totals

## Features
- Chat memory on both providers
- Token and cost counter per turn and total
- Chats saved to `chats/*.json`

## Setup
Put `GEMINI_API_KEY` and `OPENROUTER_API_KEY` in a `.env` file.