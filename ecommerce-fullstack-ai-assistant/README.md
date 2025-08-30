# AI Assistant (FastAPI + Tool-Using Agent)

A production-ready **AI Assistant** starter project built with FastAPI.
It includes:
- LLM wrapper (OpenAI-compatible)
- SQLite conversation memory per user
- Useful built-in tools: calculator, time lookup, web search (DuckDuckGo)
- FastAPI HTTP API (`/chat`) and a simple CLI client

## Quickstart

1. Clone this repo.
2. Create and activate a virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if you want live LLM responses.
4. Run:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
5. Example curl:
   ```bash
   curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" \
     -d '{"user_id":"demo","message":"What is 23*47? Also, what time is it in Tokyo?"}'
   ```

## Notes
- This is a starter; extend tools, add auth, and harden evals before production.
- Do NOT commit your `.env` containing API keys.
