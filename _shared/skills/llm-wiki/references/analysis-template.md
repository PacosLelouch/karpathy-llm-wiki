# 维护型分析页模板

用于 `wiki/analyses/` 中会随新资料持续更新的综合分析、比较、决策记录。

```markdown
---
title: 分析标题
type: analysis
mode: maintained
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
question: 原始问题或分析目标
sources: []
raw: []
tags: []
status: active
evidence_level: synthesized
---

# 分析标题

## 问题

要回答的问题或要比较的对象。

## 结论摘要

用 3-5 条 bullet 总结当前结论。

## 依据

- [[sources/...]]
- [[concepts/...]]
- [[entities/...]]

## 分析

分层展开推理、证据、限制和反例。

## 对比表

| 维度 | 方案 A | 方案 B | 备注 |
|---|---|---|---|
| ... | ... | ... | ... |

## 当前建议

> [!tip]
> 当前最可执行的建议。

## 后续问题

- [ ] ...
```
