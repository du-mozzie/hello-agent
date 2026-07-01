from helloagents import demo_react_agent


if __name__ == "__main__":
    agent = demo_react_agent()
    result = agent.run("What is (25 + 15) * 3 - 8?")
    print(result.answer)
    for step in result.steps:
        print(f"{step.type}: {step.content}")
