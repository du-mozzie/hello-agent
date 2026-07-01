"""Agent implementations from simple chat to ReAct and reflection."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .llms import BaseLLM, RuleBasedLLM
from .schema import AgentResult, Message, StepEvent
from .tools import ToolRegistry, default_registry


@dataclass
class BaseAgent:
    name: str
    llm: BaseLLM = field(default_factory=RuleBasedLLM)
    system_prompt: str = "You are a helpful AI agent."
    history: list[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.history.append(Message(role, content))  # type: ignore[arg-type]

    def messages_for(self, user_input: str) -> list[Message]:
        return [Message("system", self.system_prompt), *self.history, Message("user", user_input)]

    def run(self, user_input: str) -> AgentResult:
        raise NotImplementedError


class SimpleAgent(BaseAgent):
    """Single-call LLM agent."""

    def run(self, user_input: str) -> AgentResult:
        answer = self.llm.complete(self.messages_for(user_input))
        self.add_message("user", user_input)
        self.add_message("assistant", answer)
        return AgentResult(answer=answer, messages=list(self.history))


REACT_PROMPT = """You are a ReAct agent.

Available tools:
{tools}

Reply using exactly:
Thought: your reasoning
Action: tool_name[input] or Finish[final answer]

Question: {question}
History:
{history}
"""


class ReActAgent(BaseAgent):
    """Reasoning-and-acting agent with text tool calls."""

    def __init__(
        self,
        name: str = "react-agent",
        llm: BaseLLM | None = None,
        tools: ToolRegistry | None = None,
        max_steps: int = 5,
        system_prompt: str = "You are a careful ReAct agent.",
    ) -> None:
        super().__init__(name=name, llm=llm or RuleBasedLLM(), system_prompt=system_prompt)
        self.tools = tools or default_registry()
        self.max_steps = max_steps

    def run(self, user_input: str) -> AgentResult:
        result = AgentResult(answer="")
        scratchpad: list[str] = []
        for step in range(1, self.max_steps + 1):
            prompt = REACT_PROMPT.format(
                tools=self.tools.describe(),
                question=user_input,
                history="\n".join(scratchpad),
            )
            raw = self.llm.invoke(prompt)
            thought, action = self._parse_react(raw)
            result.steps.append(StepEvent("thought", thought, {"step": step}))
            result.steps.append(StepEvent("action", action, {"step": step}))
            if action.startswith("Finish["):
                answer = self._extract_bracket(action)
                result.answer = answer
                break
            tool_name, tool_input = self._parse_action(action)
            observation = self.tools.execute(tool_name, tool_input)
            scratchpad.extend([f"Thought: {thought}", f"Action: {action}", f"Observation: {observation}"])
            result.steps.append(StepEvent("observation", observation, {"step": step, "tool": tool_name}))
        if not result.answer:
            result.answer = scratchpad[-1].replace("Observation: ", "") if scratchpad else "No answer produced."
        self.add_message("user", user_input)
        self.add_message("assistant", result.answer)
        result.messages = list(self.history)
        return result

    @staticmethod
    def _parse_react(text: str) -> tuple[str, str]:
        thought = _match_line(text, "Thought") or "No explicit thought."
        action = _match_line(text, "Action") or f"Finish[{text.strip()}]"
        return thought, action

    @staticmethod
    def _parse_action(action: str) -> tuple[str, str]:
        match = re.match(r"\s*([A-Za-z_][\w-]*)\[(.*)\]\s*$", action, re.S)
        if not match:
            raise ValueError(f"Invalid action: {action}")
        return match.group(1), match.group(2)

    @staticmethod
    def _extract_bracket(action: str) -> str:
        return action[action.find("[") + 1 : action.rfind("]")]


class PlanAndSolveAgent(BaseAgent):
    """Agent that first drafts a plan, then solves each step."""

    def run(self, user_input: str) -> AgentResult:
        plan = self.llm.invoke(f"Create a concise plan for this task:\n{user_input}")
        answer = self.llm.invoke(f"Use this plan to answer the task.\nPlan:\n{plan}\nTask:\n{user_input}")
        result = AgentResult(answer=answer)
        result.add_step("plan", plan)
        result.add_step("solve", answer)
        self.add_message("user", user_input)
        self.add_message("assistant", answer)
        result.messages = list(self.history)
        return result


class ReflectionAgent(BaseAgent):
    """Agent that drafts, critiques, and revises an answer."""

    def run(self, user_input: str) -> AgentResult:
        draft = self.llm.invoke(user_input)
        critique = self.llm.invoke(f"Reflect on this answer and identify improvements:\n{draft}")
        final = self.llm.invoke(f"Revise the answer using the critique.\nAnswer: {draft}\nCritique: {critique}")
        result = AgentResult(answer=final)
        result.add_step("draft", draft)
        result.add_step("critique", critique)
        result.add_step("revision", final)
        self.add_message("user", user_input)
        self.add_message("assistant", final)
        result.messages = list(self.history)
        return result


def _match_line(text: str, label: str) -> str | None:
    match = re.search(rf"^{label}:\s*(.+)$", text, re.M)
    return match.group(1).strip() if match else None
