from helloagents import SimpleAgent


if __name__ == "__main__":
    agent = SimpleAgent("first-agent")
    result = agent.run("Hello, what can an agent do?")
    print(result.answer)
