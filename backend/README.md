# Smart Agent - Backend (FastAPI)

## Overview
This is the FastAPI backend for the Smart Agent. It supports:
- Reminders (stored in SQLite)
- Web search (DuckDuckGo scrape)
- News (optional via NEWSAPI_KEY)
- Fun facts
- Optional LLM integration via environment-configured providers (COHERE, GROQ, HUGGINGFACE)
- Vector memory using local Chroma (optional) with a fallback

## Run locally
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set environment variables (see `.env.example`) and run:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## Deployment
This repository includes Dockerfile and docker-compose.yml for local end-to-end deployment.

