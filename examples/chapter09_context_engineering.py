from helloagents import NoteStore, PriorityContextBuilder, WorkspaceSnapshot


if __name__ == "__main__":
    notes = NoteStore()
    notes.write("goal", "Build a detailed HelloAgents project.")
    snapshot = WorkspaceSnapshot.scan(".")
    context = (
        PriorityContextBuilder(max_chars=1200)
        .add("User Goal", "Need a complete modular implementation.", priority=100)
        .add("Notes", notes.render(), priority=80)
        .add("Workspace", snapshot.render(), priority=20)
        .build()
    )
    print(context)
