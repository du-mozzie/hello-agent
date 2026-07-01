from helloagents import DatasetBuilder, RewardFunction, TrainingPipelinePlan


if __name__ == "__main__":
    builder = DatasetBuilder()
    builder.add_sft("Solve with ReAct: 2+2", "Thought: calculate\nAction: calculator[2+2]")
    builder.add_preference("Answer clearly", "Final: 4", "maybe four")
    paths = builder.export("exports/training")
    print(paths)

    reward = RewardFunction.format_reward([r"Thought:", r"Action:"])
    print("Reward:", reward("Thought: calculate\nAction: calculator[2+2]"))
    print("\n".join(TrainingPipelinePlan("exports/training/sft.jsonl", "outputs/demo").commands()))
