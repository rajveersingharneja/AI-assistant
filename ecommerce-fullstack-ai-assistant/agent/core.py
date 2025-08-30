from typing import List, Dict, Any, Optional
from .llm import LLMClient
from .memory import MemoryStore
from .tools import TOOL_SCHEMAS, TOOL_IMPL
from models import ChatResponse
import os
import json

DEFAULT_SYSTEM = (
    "You are a helpful AI assistant. Use tools when helpful. Be concise." 
)

class Agent:
    def __init__(self):
        self.llm = LLMClient()
        self.mem = MemoryStore()
        # expose tools (schemas and impl) for potential tool-calling workflows
        self.tool_schemas = TOOL_SCHEMAS
        self.tools = TOOL_IMPL

    def _build_messages(self, user_id: str, system_prompt: Optional[str], user_message: str, limit:int=20) -> List[Dict[str, Any]]:
        history = self.mem.history(user_id, limit=limit)
        messages = []
        # system prompt
        sys_prompt = system_prompt or DEFAULT_SYSTEM
        messages.append({'role':'system', 'content': sys_prompt})
        # history
        for role, content in history:
            messages.append({'role': role, 'content': content})
        messages.append({'role':'user', 'content': user_message})
        return messages

    def handle_message(self, user_id: str, message: str, system_prompt: Optional[str]=None, temperature: float=0.2, tools_enabled: bool=True) -> ChatResponse:
        # store user message
        self.mem.add(user_id, 'user', message)
        messages = self._build_messages(user_id, system_prompt, message)
        # call LLM
        llm_resp = self.llm.chat(messages=messages, tools=(self.tool_schemas if tools_enabled else None), temperature=temperature)
        # If llm_resp is a dict with 'reply'
        reply = llm_resp.get('reply') if isinstance(llm_resp, dict) else str(llm_resp)
        # store assistant reply
        self.mem.add(user_id, 'assistant', reply)
        # rudimentary: detect simple tool call patterns (special markers)
        tool_calls = None
        used_tools = []
        # If the reply indicates a tool: we look for JSON-like tool call
        try:
            # Example: model might return {"tool":"tool_time_in","arguments":{"city":"Tokyo"}}
            parsed = None
            if isinstance(reply, str) and reply.strip().startswith('{') and reply.strip().endswith('}'):
                parsed = json.loads(reply)
            if parsed and isinstance(parsed, dict) and 'tool' in parsed:
                name = parsed['tool']
                args = parsed.get('arguments', {})
                func = self.tools.get(name)
                if func:
                    result = func(**args) if isinstance(args, dict) else func(args)
                    # store tool output
                    self.mem.add(user_id, 'tool', f"{name} -> {result}")
                    used_tools.append({'name': name, 'result': result})
                    # append tool result to messages and produce final assistant reply
                    messages.append({'role':'tool', 'content': result})
                    final = self.llm.chat(messages=messages, temperature=temperature)
                    final_reply = final.get('reply') if isinstance(final, dict) else str(final)
                    self.mem.add(user_id, 'assistant', final_reply)
                    return ChatResponse(reply=final_reply, tool_calls=[{'name':name,'arguments':args}], used_tools=used_tools)
        except Exception:
            pass

        return ChatResponse(reply=reply, tool_calls=tool_calls, used_tools=(used_tools or None))
