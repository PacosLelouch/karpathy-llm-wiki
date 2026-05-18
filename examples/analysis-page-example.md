---
title: MapGen 生成管线分析
type: analysis
mode: maintained
topic:
  - map-generation
created: 2026-05-18
updated: 2026-05-18
question: MapGen 当前地图生成流程的核心阶段是什么？
sources:
  - [[sources/map-generator-notes]]
raw:
  - raw/sources/2026-05-18-map-generator-notes.md
tags:
  - pcg
  - pipeline
status: active
evidence_level: synthesized
---

# MapGen 生成管线分析

## 问题

MapGen 当前地图生成流程的核心阶段是什么？各阶段之间如何影响生成结果？

## 结论摘要

- 当前管线可抽象为：约束输入 → 规则驱动布局 → 后处理 → 约束解释。
- 后处理负责连通性和节奏，但也可能掩盖布局阶段的结构问题。
- 可解释性应贯穿生成与验证，而不是只在最后生成说明。

## 依据

- [[sources/map-generator-notes]]
- [[concepts/constraint-driven-generation]]
- [[entities/mapgen]]

## 分析

MapGen 的设计目标包含可控生成和结果解释，因此生成管线应把“约束”作为一等对象处理。若约束只在后处理阶段检查，系统可能能修复局部连通性，却无法解释全局结构为什么合理。

## 对比表

| 阶段 | 输入 | 输出 | 风险 |
|---|---|---|---|
| 约束输入 | 设计目标、参数、规则 | 可验证约束 | 约束过强或不可满足 |
| 规则布局 | 房间规则、拓扑目标 | 初始地图 | 重复形状、结构弱 |
| 后处理 | 初始地图、连通性要求 | 修正地图 | 破坏原始设计意图 |
| 约束解释 | 地图、约束、验证结果 | 满足/违反说明 | 解释与真实生成逻辑脱节 |

## 当前建议

> [!tip]
> 优先把约束验证器独立出来，让布局和后处理都能调用同一套验证逻辑。

## 后续问题

- [ ] 是否存在硬约束/软约束区分？
- [ ] 是否需要记录每次后处理修改的原因？
