from helloagents import PlanAndSolveAgent, ReActAgent, ReflectionAgent, SimpleAgent


if __name__ == "__main__":
    question = "What is (12 + 8) * 2?"
    for agent in [
        SimpleAgent("simple"),
        ReActAgent("react", max_steps=3),
        PlanAndSolveAgent("planner"),
        ReflectionAgent("reflector"),
    ]:
        result = agent.run(question)
        print(f"\n[{agent.name}] {result.answer}")
        for step in result.steps:
            print(f"- {step.type}: {step.content}")
