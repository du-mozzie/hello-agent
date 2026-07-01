from helloagents import ReActAgent, Tool, ToolRegistry


def reverse_text(text: str) -> str:
    return text[::-1]


if __name__ == "__main__":
    registry = ToolRegistry()
    registry.register(Tool("reverse", "Reverse input text.", reverse_text))
    registry.register_function("echo", "Return input unchanged.", lambda text: text)
    agent = ReActAgent("framework-agent", tools=registry)
    print(registry.describe())
    print(agent.run("Use a tool if useful.").answer)
