from helloagents import CyberTown


if __name__ == "__main__":
    town = CyberTown()
    print("\n".join(town.tick("morning planning meeting")))
    print(town.interact("Alex", "Blair", "research plan"))
    print(town.summary())
