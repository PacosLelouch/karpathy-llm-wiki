# 实体页模板

用于 `wiki/entities/`，记录人物、组织、工具、项目、算法、游戏、引擎等实体。

```markdown
---
title: 名称
type: entity
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
raw: []
tags: []
status: stub | active | mature | outdated | conflicting
evidence_level: synthesized
mode: maintained
---

# 名称

## 简述

一句到一段话定义该实体。

## 当前综合理解

跨来源综合说明该实体是什么、做什么、为何重要、在主题中的位置。

## 关键事实/观点

- 事实或观点。来源：[[sources/...]]

## 关系与交叉引用

- 相关实体：[[entities/...]]
- 相关概念：[[concepts/...]]
- 相关分析：[[analyses/...]]

## 争议、矛盾或版本变化

> [!warning] 冲突或版本变化
> 记录不同来源的差异、时间和当前判断。

## 待研究问题

- [ ] ...
```
