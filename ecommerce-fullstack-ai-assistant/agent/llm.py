import os
from typing import List, Dict, Any, Optional
try:
    # openai Python package
    import openai
except Exception:
    openai = None

class LLMClient:
    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None):
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL')
        self.api_key = os.getenv('OPENAI_API_KEY')

    def chat(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.2) -> Dict[str, Any]:
        """Make a chat call to the LLM provider. If OPENAI_API_KEY is not set, returns a canned reply for testing."""
        if not self.api_key or openai is None:
            # fallback canned response (useful for offline testing)
            return {
                'reply': 'API key not configured. This is an offline canned reply. To enable live LLM responses, set OPENAI_API_KEY in your environment.',
                'tool_calls': None
            }
        # Basic OpenAI ChatCompletion style call; adapt based on your provider SDK
        try:
            openai.api_key = self.api_key
            if self.base_url:
                openai.api_base = self.base_url
            # Build messages for OpenAI's ChatCompletion API
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=512
            )
            text = resp.choices[0].message.get('content') if resp.choices else ''
            return {'reply': text, 'tool_calls': None}
        except Exception as e:
            return {'reply': f'LLM error: {e}', 'tool_calls': None}
