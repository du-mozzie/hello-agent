from helloagents import (
    DatasetBuilder,
    FunctionCallCase,
    FunctionCallEvaluator,
    NegotiationOffer,
    PairwiseJudge,
    PriorityContextBuilder,
    RoundRobinLoadBalancer,
    SimpleNegotiator,
    TaskDistributor,
    TrainingPipelinePlan,
    TravelPlanner,
)


def test_priority_context_builder_keeps_high_priority_content():
    context = (
        PriorityContextBuilder(max_chars=60)
        .add("low", "x" * 100, priority=1)
        .add("high", "important", priority=100)
        .build()
    )
    assert "important" in context
    assert "xxx" not in context


def test_task_distributor_and_balancer():
    distributor = TaskDistributor()
    distributor.register("coder", ["debug", "test"])
    assert distributor.assign("debug test failure") == "coder"
    balancer = RoundRobinLoadBalancer(["a", "b"])
    assert [balancer.next(), balancer.next(), balancer.next()] == ["a", "b", "a"]


def test_negotiator_chooses_best_offer():
    negotiator = SimpleNegotiator({"quality": 1.0, "cost": -1.0})
    offer = negotiator.choose(
        [
            NegotiationOffer("expensive", {"quality": 1.0, "cost": 0.9}),
            NegotiationOffer("balanced", {"quality": 0.8, "cost": 0.1}),
        ]
    )
    assert offer.sender == "balanced"


def test_function_call_evaluator():
    case = FunctionCallCase("calculate", "calculator", {"expression": "2+2"})
    result = FunctionCallEvaluator().evaluate_prediction(
        '{"name":"calculator","arguments":{"expression":"2+2"}}',
        case,
    )
    assert result["passed"] is True


def test_pairwise_judge_returns_winner():
    result = PairwiseJudge().judge("agent memory", "agent memory stores context", "unrelated")
    assert result.winner == "A"


def test_training_pipeline_plan_and_dataset_builder(tmp_path):
    builder = DatasetBuilder()
    builder.add_sft("prompt", "response")
    builder.add_preference("prompt", "chosen", "rejected")
    paths = builder.export(tmp_path)
    assert paths["sft"].exists()
    assert "sft-train" in TrainingPipelinePlan(str(paths["sft"]), "out").commands()[1]


def test_travel_planner_structured_plan():
    plan = TravelPlanner().build_plan("Shanghai", "museums, coffee", days=2)
    assert len(plan.days) == 2
    assert "Shanghai" in plan.to_markdown()
