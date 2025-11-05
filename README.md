

# Smart Agent (React + FastAPI) 

This project contains:
- `backend/` - FastAPI server
- `frontend/` - React app

## Quick start (local, with Docker)
1. Copy `.env.example` files into `backend/.env` and `frontend/.env` and fill API keys as needed.
2. Create `.env` in the root (for docker-compose) with variables:
   - NEWSAPI_KEY
   - COHERE_API_KEY
   - GROQ_API_KEY
   - HUGGINGFACE_API_KEY
   - USE_PROVIDER (COHERE | GROQ | HUGGINGFACE)
   - REACT_APP_API_BASE (default http://localhost:8000)
3. Run:
   ```bash
   docker-compose up --build
   ```
4. Open frontend: http://localhost:3000
   Backend: http://localhost:8000


>>>>>>> 40cc560 (Initial commit)
