---
title: Map Generator Notes
type: source
date: Unknown
ingested: 2026-05-18
author: MapGen Team
source_path: raw/sources/2026-05-18-map-generator-notes.md
raw:
  - raw/sources/2026-05-18-map-generator-notes.md
topic:
  - map-generation
tags:
  - pcg
  - mapgen
status: active
evidence_level: primary
---

# Map Generator Notes

## 摘要

该来源描述了 MapGen 原型的地图生成管线：规则驱动房间放置、连通性与节奏后处理，以及当前在房间形状重复和全局结构较弱方面的不足。

## 关键要点

- 原型结合规则驱动房间放置与后处理流程。来源：原文第 1 段。
- 当前弱点包括房间形状重复和全局结构不足。来源：原文第 1 段。
- 设计者希望生成前可编辑约束，生成后能解释约束满足/违反原因。来源：原文第 2 段。

## 关键证据/引用

- “rule-based room placement with post-processing passes for connectivity and pacing” — 原文第 1 段。

## 涉及实体

- [[entities/mapgen]] — 项目实体。

## 涉及概念

- [[concepts/rule-based-map-generation]] — 规则驱动地图生成。
- [[concepts/constraint-driven-generation]] — 约束驱动生成。

## 对既有 wiki 的影响

- 支持：MapGen 当前偏规则驱动和后处理管线。
- 新增：需要解释生成结果为何满足或违反约束。
- 冲突：暂无。

## 待验证问题

- [ ] 约束编辑发生在生成前的哪个阶段？
- [ ] 后处理是否会破坏设计者指定的硬约束？
