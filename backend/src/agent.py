from backend.src.agent.basic.router_agent import RouterAgent

if __name__ == "__main__":
    router = RouterAgent()
    while True:
        user_prompt = input("🗨️ You: ")
        if user_prompt.lower() in ("exit", "quit"):
            break
        response = router.run(user_prompt)
        print(f"🤖 Assistant: {response}\n")