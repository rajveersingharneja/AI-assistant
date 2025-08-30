from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Stable user identifier for memory")
    message: str
    system_prompt: Optional[str] = None
    temperature: float = 0.2
    tools_enabled: bool = True

class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class ChatResponse(BaseModel):
    reply: str
    tool_calls: Optional[List[ToolCall]] = None
    used_tools: Optional[List[Dict[str, Any]]] = None
