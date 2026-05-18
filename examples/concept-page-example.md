---
title: 约束驱动生成
type: concept
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
  - constraints
status: active
evidence_level: synthesized
mode: maintained
---

# 约束驱动生成

## 简述

约束驱动生成是一类程序化内容生成方法：先表达设计约束，再让生成器在约束空间内搜索、构造或修正内容。

## 当前综合理解

在 MapGen 语境中，约束驱动生成不仅要求地图满足连通性、节奏、房间分布等条件，还要求系统能解释生成结果为何满足或违反这些条件。它适合设计师需要可控性、可调参和可诊断反馈的地图生成流程。

## 关键事实/观点

- 设计者希望约束能在生成前编辑，并在生成后获得解释。来源：[[sources/map-generator-notes]]
- 约束可能分为硬约束和软约束，后处理阶段需要避免破坏硬约束。来源：[[sources/map-generator-notes]] 的待验证问题。

## 适用场景

- 需要设计师明确控制地图结构。
- 需要解释生成失败原因。
- 需要在自动生成与人工调参之间建立反馈循环。

## 局限与误区

- 约束过强可能导致生成空间过小。
- 只在后处理阶段修补约束，可能掩盖生成器本身的结构问题。

## 关系与交叉引用

- 相关概念：[[concepts/rule-based-map-generation]]
- 相关实体：[[entities/mapgen]]

## 争议、矛盾或版本变化

> [!warning]
> 当前证据主要来自单个设计笔记，尚缺少实际系统实现或评测数据。

## 待研究问题

- [ ] MapGen 的约束语言是显式规则、参数表，还是自然语言？
- [ ] 约束解释是否由生成器直接产生，还是由独立验证器产生？
