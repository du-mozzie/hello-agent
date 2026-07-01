# 第 2 章：智能体发展史

## 学习目标

通过 ELIZA 理解早期智能体如何使用规则、正则匹配、模板回复和代词转换完成对话。

## 对应实现

- `helloagents.fundamentals.ElizaBot`

## 运行示例

```powershell
python examples/chapter02_eliza.py
```

## 代码要点

`ElizaBot` 不具备真正理解能力，但可以展示“规则驱动智能体”的工作方式。这有助于理解为什么现代 Agent 需要语言模型、工具和记忆。

## 扩展方向

可以增加中文规则库，或把 ELIZA 作为规则兜底模块，用于处理固定 FAQ 和安全提示。
