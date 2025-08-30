import math
from dateutil import tz
from datetime import datetime
from duckduckgo_search import DDGS

def tool_calculator(expression: str) -> str:
    allowed_names = {'sqrt': math.sqrt, 'pow': pow, 'abs': abs}
    # minimal safe eval: allow digits, operators and parentheses and known names
    try:
        code = compile(expression, '<string>', 'eval')
        for name in code.co_names:
            if name not in allowed_names:
                raise ValueError(f'Use of name "{name}" not allowed')
        result = eval(code, {'__builtins__': {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f'Error evaluating expression: {e}'

def tool_time_in(city: str) -> str:
    TZ = {
        'tokyo': 'Asia/Tokyo',
        'delhi': 'Asia/Kolkata',
        'mumbai': 'Asia/Kolkata',
        'new york': 'America/New_York',
        'london': 'Europe/London',
        'paris': 'Europe/Paris',
        'sydney': 'Australia/Sydney',
    }
    zone = TZ.get(city.lower())
    if not zone:
        return 'Unknown city. Try: Tokyo, Delhi, New York, London, Paris, Sydney.'
    now = datetime.now(tz.gettz(zone))
    return now.strftime('%Y-%m-%d %H:%M (%Z)')

def tool_search(query: str, max_results: int = 5) -> str:
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"- {r.get('title')}\n  {r.get('href')}\n  {r.get('body')}")
    except Exception as e:
        return f"Search error: {e}"
    if not results:
        return 'No results.'
    return '\n'.join(results)

def tool_echo(text: str) -> str:
    return text

TOOL_SCHEMAS = [
    {
        'type': 'function',
        'function': {
            'name': 'tool_calculator',
            'description': 'Evaluate a math expression (+,-,*,/,**,%, parentheses).',
            'parameters': {
                'type': 'object',
                'properties': {
                    'expression': {'type': 'string'}
                },
                'required': ['expression']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'tool_time_in',
            'description': 'Get current local time in a known city.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'city': {'type': 'string'}
                },
                'required': ['city']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'tool_search',
            'description': 'Search via DuckDuckGo.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string'},
                    'max_results': {'type': 'integer'}
                },
                'required': ['query']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'tool_echo',
            'description': 'Echo text back.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {'type': 'string'}
                },
                'required': ['text']
            }
        }
    }
]

TOOL_IMPL = {
    'tool_calculator': tool_calculator,
    'tool_time_in': tool_time_in,
    'tool_search': tool_search,
    'tool_echo': tool_echo,
}
