# 第 13 章：智能旅行助手

## 学习目标

把 Agent 能力组合成面向用户任务的旅行规划应用。

## 对应实现

- `TravelPlanner`
- `TripPlan`
- `TripDay`

## 运行示例

```powershell
python examples/chapter13_trip_planner.py
```

## 代码要点

`TravelPlanner.build_plan()` 返回结构化计划，`to_markdown()` 负责文本展示。结构化输出更适合 UI、API 和评估。

## 扩展方向

接入地图、POI、天气、预算、交通路线和酒店信息。
