# Chapter 10 - Agent Communication Protocols

## Goal

Prototype MCP-style tool calls, agent-to-agent messaging, service discovery, task distribution, load balancing, and negotiation.

## Implemented Code

- `MCPToolAdapter`
- `A2AAgent`
- `ANPRegistry`
- `TaskDistributor`
- `RoundRobinLoadBalancer`
- `SimpleNegotiator`

## Run

```powershell
python examples/chapter10_protocols.py
```

## Extension

Replace the local adapters with real MCP servers, HTTP transports, authentication, and durable queues.
