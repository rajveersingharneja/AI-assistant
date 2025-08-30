import os
from fastapi import FastAPI, HTTPException
from models import ChatRequest, ChatResponse
from agent.core import Agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Assistant")

# single global agent instance (simple for starter)
agent = Agent()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        resp = agent.handle_message(
            user_id=req.user_id,
            message=req.message,
            system_prompt=req.system_prompt,
            temperature=req.temperature,
            tools_enabled=req.tools_enabled
        )
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status":"ok"}
