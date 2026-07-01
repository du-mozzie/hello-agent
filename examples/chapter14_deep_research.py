from helloagents import DeepResearchAgent


if __name__ == "__main__":
    corpus = {
        "context": "Context engineering selects and compresses relevant information for the next model call.",
        "memory": "Agent memory includes working, episodic, and semantic stores.",
        "protocol": "Agent protocols coordinate tool use and peer communication.",
    }
    print(DeepResearchAgent(corpus).research("agent memory and context engineering"))
