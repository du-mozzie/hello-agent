# Protocols Module

Module: `helloagents.protocols`

This module models the communication layer introduced in the tutorial.

## Protocols

- `MCPToolAdapter`: exposes a local `Tool` through a minimal MCP-like call schema.
- `A2AAgent`: sends direct messages between peer agents.
- `ANPRegistry`: publishes and discovers named services.
- `TaskDistributor`: assigns tasks to agents by capability keyword.
- `RoundRobinLoadBalancer`: balances requests across equivalent workers.
- `SimpleNegotiator` and `NegotiationOffer`: choose offers by weighted utility.

## Example

```python
from helloagents import A2AAgent, SimpleAgent

alice = A2AAgent(SimpleAgent("alice"))
bob = A2AAgent(SimpleAgent("bob"))
reply = alice.send(bob, "Summarize your role.")
print(reply.content)
```

## Production Mapping

Use `MCPToolAdapter` as the local contract before replacing it with a real MCP server/client. Use `A2AAgent` and `ANPRegistry` to prototype multi-agent collaboration and service discovery.

## Communication Layers

Local prototypes can call Python objects directly. Production systems normally add transport, authentication, schema validation, retries, idempotency, and durable queues. The module keeps those concerns explicit so they can be introduced without rewriting agent logic.
