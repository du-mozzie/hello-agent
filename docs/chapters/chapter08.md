# 第 8 章：记忆与检索

## 学习目标

掌握工作记忆、会话记忆、情节记忆、向量检索和 RAG 的基本实现方式。

## 对应实现

- `WorkingMemory`
- `ConversationMemory`
- `EpisodicMemory`
- `VectorMemory`
- `MemoryConsolidator`
- `RAGPipeline`
- `RAGQAAssistant`

## 运行示例

```powershell
python examples/chapter08_memory_rag.py
```

## 代码要点

短期状态先进入工作记忆，重要信息可以固化到向量记忆中。回答问题前通过 RAG 检索相关上下文。

## 扩展方向

接入真实文档解析、embedding 模型、向量数据库和引用溯源。
