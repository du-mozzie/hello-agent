from helloagents.lowcode import PlatformAdapter, hello_agent_flow


if __name__ == "__main__":
    flow = hello_agent_flow()
    for platform in ["dify", "coze", "fastgpt", "n8n"]:
        path = f"exports/{platform}-hello-agent.json"
        PlatformAdapter(platform).export(flow, path)
        print(path)
