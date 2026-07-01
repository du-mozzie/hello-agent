from helloagents import A2AAgent, SimpleAgent


if __name__ == "__main__":
    product_manager = A2AAgent(SimpleAgent("product-manager"))
    engineer = A2AAgent(SimpleAgent("engineer"))
    reply = product_manager.send(engineer, "Draft a tiny implementation plan for an agent framework.")
    print(reply.content)
