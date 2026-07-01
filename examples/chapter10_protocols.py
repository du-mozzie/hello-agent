from helloagents import (
    ANPRegistry,
    NegotiationOffer,
    RoundRobinLoadBalancer,
    SimpleNegotiator,
    TaskDistributor,
)


if __name__ == "__main__":
    registry = ANPRegistry()
    registry.publish("research-agent", object())
    registry.publish("coding-agent", object())
    print("Discovered:", registry.discover("agent"))

    distributor = TaskDistributor()
    distributor.register("research-agent", ["research", "search", "summarize"])
    distributor.register("coding-agent", ["code", "test", "debug"])
    print("Assigned:", distributor.assign("debug code test"))

    balancer = RoundRobinLoadBalancer(["worker-a", "worker-b"])
    print("Workers:", [balancer.next(), balancer.next(), balancer.next()])

    negotiator = SimpleNegotiator({"quality": 0.7, "cost": -0.3})
    offer = negotiator.choose(
        [
            NegotiationOffer("agent-a", {"quality": 0.8, "cost": 0.4}),
            NegotiationOffer("agent-b", {"quality": 0.7, "cost": 0.1}),
        ]
    )
    print("Best offer:", offer.sender)
