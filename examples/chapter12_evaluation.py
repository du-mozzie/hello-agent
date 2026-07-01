from helloagents import Evaluator, FunctionCallCase, FunctionCallEvaluator, PairwiseJudge, SimpleAgent, TaskCase


if __name__ == "__main__":
    report = Evaluator().evaluate(SimpleAgent("eval-agent"), [TaskCase("Hello", "deterministic", "contains")])
    print(report.to_markdown())

    call_case = FunctionCallCase("calculate 2+2", "calculator", {"expression": "2+2"})
    print(FunctionCallEvaluator().evaluate_prediction('{"name":"calculator","arguments":{"expression":"2+2"}}', call_case))

    print(PairwiseJudge().judge("explain agent memory", "agent memory stores context", "short answer"))
