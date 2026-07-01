# 记忆与检索

模块：`helloagents.memory`

记忆模块提供短期记忆、长期事件记忆、向量检索和 RAG 流水线，是构建长期任务智能体的基础。

## 组件

- `WorkingMemory`：有限长度的短期工作记忆。
- `ConversationMemory`：会话窗口和压缩摘要。
- `EpisodicMemory`：追加式事件记忆。
- `VectorMemory`：基于词袋相似度的本地向量检索。
- `MemoryConsolidator`：把短期观察固化到长期可检索记忆。
- `RAGPipeline`：文档写入、检索上下文、构造问答提示。
- `RAGQAAssistant`：基于检索结果的简单 QA 封装。

## 示例

```python
from helloagents import RAGPipeline, VectorMemory

rag = RAGPipeline(VectorMemory())
rag.ingest({"react": "ReAct combines reasoning and tool use."})
print(rag.retrieve_context("tool reasoning"))
```

## 推荐流程

1. 用 `WorkingMemory` 保存当前任务状态。
2. 用 `ConversationMemory` 保存最近对话和摘要。
3. 用 `MemoryConsolidator` 定期把重要信息写入 `VectorMemory`。
4. 用 `RAGPipeline` 在模型调用前检索相关上下文。
5. 用评估模块验证检索质量和最终答案。

## 扩展建议

当前 `VectorMemory` 是教学实现。真实项目中可以替换为 FAISS、Milvus、pgvector、Elasticsearch 或云向量数据库。
