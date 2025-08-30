import json
from models import ChatRequest
from agent.core import Agent

agent = Agent()

def main():
    print("Simple AI Assistant CLI. Type 'exit' to quit.")
    user_id = "cli-user"
    while True:
        msg = input("> ")
        if not msg:
            continue
        if msg.strip().lower() in ("exit","quit"):
            break
        req = ChatRequest(user_id=user_id, message=msg)
        resp = agent.handle_message(user_id=req.user_id, message=req.message,
                                    system_prompt=req.system_prompt, temperature=req.temperature,
                                    tools_enabled=req.tools_enabled)
        print("\nAssistant:", resp.reply)
        if resp.tool_calls:
            print("Tool calls:", resp.tool_calls)
        print("")

if __name__ == '__main__':
    main()
