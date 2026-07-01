"""Command line interface for examples."""

from __future__ import annotations

import argparse

from .applications import CyberTown, DeepResearchAgent, TravelPlanner, demo_react_agent


def main() -> None:
    parser = argparse.ArgumentParser(prog="helloagents")
    sub = parser.add_subparsers(dest="command", required=True)

    react = sub.add_parser("react")
    react.add_argument("question")

    travel = sub.add_parser("travel")
    travel.add_argument("destination")
    travel.add_argument("interests")
    travel.add_argument("--days", type=int, default=3)

    research = sub.add_parser("research")
    research.add_argument("topic")

    sub.add_parser("town")

    args = parser.parse_args()
    if args.command == "react":
        print(demo_react_agent().run(args.question).answer)
    elif args.command == "travel":
        print(TravelPlanner().plan(args.destination, args.interests, args.days))
    elif args.command == "research":
        corpus = {
            "memory": "Agent memory stores working, episodic, and semantic knowledge.",
            "context": "Context engineering selects the most relevant state for the next model call.",
        }
        print(DeepResearchAgent(corpus).research(args.topic))
    elif args.command == "town":
        town = CyberTown()
        town.tick()
        print(town.summary())


if __name__ == "__main__":
    main()
