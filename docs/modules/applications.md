# Applications Module

Module: `helloagents.applications`

This module contains compact implementations of the tutorial's larger projects.

## Applications

- `TravelPlanner`: creates a multi-day itinerary from destination and interests.
- `TripPlan` and `TripDay`: structured travel output.
- `DeepResearchAgent`: plans, retrieves local evidence, and synthesizes a research brief.
- `ResearchReport`: structured research output.
- `CyberTown`: simulates multiple town residents with episodic memory.
- `demo_react_agent()`: preconfigured ReAct agent with calculator and local search.

## Example

```python
from helloagents import TravelPlanner

print(TravelPlanner().plan("Shanghai", "museums, coffee, river walk", days=2))
```

These demos are intentionally small so they can run offline. Replace their services with real maps, web search, databases, or game engines as needed.

## Application Architecture

Each application keeps a structured method, such as `build_plan()` or `build_report()`, and a Markdown rendering method. This separation is deliberate: UI, API, and evaluation code should consume structured data instead of scraping text.
