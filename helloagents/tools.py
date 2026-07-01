"""Tool abstractions and built-in tools."""

from __future__ import annotations

import ast
import math
import operator
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


class ToolError(RuntimeError):
    """Raised when a tool cannot be executed."""


@dataclass(slots=True)
class Tool:
    name: str
    description: str
    func: Callable[[str], str]

    def run(self, input_text: str) -> str:
        return str(self.func(input_text))


class ToolRegistry:
    """Registry and execution facade for tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> Tool:
        if not tool.name:
            raise ValueError("Tool name cannot be empty.")
        self._tools[tool.name] = tool
        return tool

    def register_function(self, name: str, description: str, func: Callable[[str], str]) -> Tool:
        return self.register(Tool(name=name, description=description, func=func))

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise ToolError(f"Unknown tool: {name}") from exc

    def execute(self, name: str, input_text: str) -> str:
        try:
            return self.get(name).run(input_text)
        except Exception as exc:
            if isinstance(exc, ToolError):
                raise
            raise ToolError(f"Tool {name} failed: {exc}") from exc

    def describe(self) -> str:
        return "\n".join(f"- {tool.name}: {tool.description}" for tool in self._tools.values())

    def names(self) -> list[str]:
        return list(self._tools)

    def __len__(self) -> int:
        return len(self._tools)


def safe_calculate(expression: str) -> int | float:
    """Evaluate a small arithmetic expression without eval."""

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    functions = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log}
    constants = {"pi": math.pi, "e": math.e}

    def walk(node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](walk(node.operand))
        if isinstance(node, ast.Name) and node.id in constants:
            return constants[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in functions:
            return functions[node.func.id](*[walk(arg) for arg in node.args])
        raise ToolError(f"Unsupported expression: {expression}")

    tree = ast.parse(expression, mode="eval")
    return walk(tree.body)


def calculator_tool() -> Tool:
    return Tool("calculator", "Safely evaluate arithmetic expressions.", lambda text: str(safe_calculate(text)))


def local_search_tool(documents: dict[str, str] | None = None) -> Tool:
    docs = documents or {
        "agent": "An agent perceives context, reasons about goals, uses tools, and acts.",
        "react": "ReAct alternates reasoning traces with tool actions and observations.",
        "rag": "RAG retrieves external knowledge before generating an answer.",
    }

    def search(query: str) -> str:
        terms = {term.lower() for term in query.split() if term.strip()}
        scored = []
        for title, body in docs.items():
            score = sum(1 for term in terms if term in title.lower() or term in body.lower())
            if score:
                scored.append((score, title, body))
        if not scored:
            return "No local document matched the query."
        scored.sort(reverse=True)
        return "\n".join(f"{title}: {body}" for _, title, body in scored[:3])

    return Tool("local_search", "Search a small in-memory document collection.", search)


def terminal_tool(workdir: str | Path = ".", allowed: set[str] | None = None) -> Tool:
    allowed_commands = allowed or {"python", "pytest", "dir", "echo"}
    base = Path(workdir).resolve()

    def run(command: str) -> str:
        first = command.strip().split(maxsplit=1)[0]
        if first not in allowed_commands:
            raise ToolError(f"Command is not allowed: {first}")
        completed = subprocess.run(
            command,
            cwd=base,
            shell=True,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        output = (completed.stdout + completed.stderr).strip()
        return output or f"Command exited with code {completed.returncode}."

    return Tool("terminal", "Run an allow-listed local shell command.", run)


def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(calculator_tool())
    registry.register(local_search_tool())
    return registry
