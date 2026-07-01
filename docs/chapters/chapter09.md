# Chapter 09 - Context Engineering

## Goal

Assemble model context from user goals, notes, working memory, retrieved content, and workspace state while respecting a token budget.

## Implemented Code

- `NoteStore`
- `WorkspaceSnapshot`
- `ContextBuilder`
- `PriorityContextBuilder`

## Run

```powershell
python examples/chapter09_context_engineering.py
```

## Extension

Add token counting for the target model and define retention policies for instructions, recent messages, tool results, and retrieved documents.
