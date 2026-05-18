---
title: WFC 与 BSP 地图生成比较归档
type: archive
mode: archive
topic:
  - map-generation
created: 2026-05-18
updated: 2026-05-18
archived: 2026-05-18
question: WFC 和 BSP 哪种更适合 MapGen？
sources:
  - [[concepts/wave-function-collapse]]
  - [[concepts/binary-space-partitioning]]
tags:
  - pcg
  - archive
status: active
evidence_level: synthesized
---

# WFC 与 BSP 地图生成比较归档

> [!info] Archive
> 这是一次问答的时间点快照。后续新资料进入 wiki 时，不会自动改写本页；如依据页面发生重大变化，应在巡检中报告。

## 原始问题

WFC 和 BSP 哪种更适合 MapGen？

## 结论摘要

- BSP 更适合需要清晰房间分割、层级空间结构和可控布局的早期 MapGen 原型。
- WFC 更适合局部模式约束强、需要从样例中扩展结构的生成任务。
- 如果 MapGen 的重点是“设计师可解释约束”，BSP 或规则布局更容易作为基础管线。

## 依据页面

- [[concepts/wave-function-collapse]]
- [[concepts/binary-space-partitioning]]

## 归档内容

BSP 的优势在于空间划分过程直接对应可解释的设计操作：切分、房间生成、连接、后处理。WFC 的优势在于模式一致性，但解释“为什么生成这个全局结构”通常更困难。

## 不确定性

- 当前结论依赖已有 wiki 页面；若后续加入 WFC 可解释性或混合管线资料，需要重新评估。

## 后续问题

- [ ] 是否存在 BSP + WFC 的混合管线？
