---
title: MapGen
type: entity
topic:
  - map-generation
created: 2026-05-18
updated: 2026-05-18
sources:
  - [[sources/map-generator-notes]]
raw:
  - raw/sources/2026-05-18-map-generator-notes.md
tags:
  - pcg
  - tool
status: active
evidence_level: synthesized
mode: maintained
---

# MapGen

## 简述

MapGen 是一个围绕程序化地图生成的研究/项目实体，当前关注规则驱动房间放置、后处理、可编辑约束和结果解释。

## 当前综合理解

现有资料显示，MapGen 的核心挑战不是单纯生成地图，而是在生成可控性、结构多样性、连通性、节奏和可解释性之间取得平衡。

## 关键事实/观点

- 原型包含规则驱动房间放置和连通性/节奏后处理。来源：[[sources/map-generator-notes]]
- 当前弱点包括房间形状重复和全局结构弱。来源：[[sources/map-generator-notes]]

## 关系与交叉引用

- 相关概念：[[concepts/rule-based-map-generation]]
- 相关概念：[[concepts/constraint-driven-generation]]
- 相关分析：[[analyses/mapgen-generation-pipeline]]

## 争议、矛盾或版本变化

> [!warning]
> 目前还无法判断 MapGen 是实际产品、研究原型还是文档主题；需补充来源。

## 待研究问题

- [ ] MapGen 的目标用户是设计师、研究者还是运行时系统？
- [ ] 当前管线是否已有可运行实现？
