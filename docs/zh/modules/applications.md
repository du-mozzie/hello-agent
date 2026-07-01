# 综合应用

模块：`helloagents.applications`

该模块实现教程后半部分的综合项目，以较小代码量展示如何组合 Agent、工具、记忆、检索、评估和应用结构。

## 应用

- `TravelPlanner`：根据目的地和兴趣生成多日旅行计划。
- `TripPlan` / `TripDay`：结构化旅行计划输出。
- `DeepResearchAgent`：规划、检索本地证据并生成研究报告。
- `ResearchReport`：结构化研究报告。
- `CyberTown`：多角色小镇模拟，包含事件记忆和关系变化。
- `demo_react_agent()`：预配置 ReAct Agent，内置计算器和本地搜索。

## 示例

```python
from helloagents import TravelPlanner

planner = TravelPlanner()
plan = planner.build_plan("Shanghai", "museums, coffee", days=2)
print(plan.to_markdown())
```

## 结构化输出

应用层通常同时提供：

- `build_*()`：返回结构化对象，适合 API、UI 和评估。
- `to_markdown()` 或 `plan()`：返回可读文本，适合命令行和文档展示。

这种分离可以避免下游系统解析自然语言文本。

## 扩展建议

- 旅行助手可接入地图、POI、天气和路线规划。
- 深度研究可接入 Web 搜索、引用抽取和报告导出。
- 赛博小镇可接入前端或游戏引擎，增加地点、日程、关系网络和长期记忆。
