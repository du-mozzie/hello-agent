from helloagents import DeepResearchAgent, Evaluator, ReActAgent, TaskCase, TravelPlanner


if __name__ == "__main__":
    agent = ReActAgent(max_steps=3)
    eval_report = Evaluator().evaluate(agent, [TaskCase("What is (10 + 5) * 2?", "30", "contains")])
    trip = TravelPlanner().plan("Hangzhou", "lake walk, tea culture", days=2)
    research = DeepResearchAgent({"agent": "A complete agent project needs tools, memory, context, and evaluation."})
    print(eval_report.to_markdown())
    print(trip)
    print(research.research("complete agent project"))
