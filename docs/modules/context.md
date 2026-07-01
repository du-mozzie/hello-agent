# Context Module

Module: `helloagents.context`

Context engineering decides what information should enter the next model call.

## Components

- `NoteStore`: named notes for long-running tasks.
- `WorkspaceSnapshot`: file-list snapshot of a project.
- `ContextBuilder`: bounded section composer for prompts.
- `PriorityContextBuilder`: keeps high-priority sections when the context budget is tight.
- `ContextItem`: title/content/priority record.

## Example

```python
from helloagents import ContextBuilder, NoteStore

notes = NoteStore()
notes.write("goal", "Build a ReAct demo.")
context = ContextBuilder(max_chars=1000).add_notes(notes).build()
print(context)
```

## Recommended Flow

Collect stable instructions, active user request, recent conversation, working memory, retrieved knowledge, and relevant workspace facts. Then trim by priority before calling the model.

## Priority Policy

Use high priority for system instructions and the active user request, medium priority for recent tool observations and working memory, and lower priority for broad workspace summaries. This mirrors production context engineering where not all available data should enter every model call.
