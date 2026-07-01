from helloagents import ElizaBot


if __name__ == "__main__":
    bot = ElizaBot(seed=1)
    for text in ["I need better tools", "I am curious about agents", "Tell me more"]:
        print(f"You: {text}")
        print(f"ELIZA: {bot.respond(text)}")
