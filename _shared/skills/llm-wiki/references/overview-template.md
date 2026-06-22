# overview.md 模板

用于 `wiki/overview.md`，作为领域入口页。职责：概述全貌、导航到专题页面、列出开放问题。不重复 concept 或 analysis 页面的具体内容。

```markdown
---
title: 领域名称概览
type: overview
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
status: active
---

# 领域名称概览

## 一句话概述

一段话说明这个 wiki 关注的领域和当前核心认知。

## 核心主题

按主题分组，链接到相关页面：

### 主题一

- [[concepts/...]] — 一句话说明
- [[entities/...]] — 一句话说明

### 主题二

- [[concepts/...]] — 一句话说明
- [[analyses/...]] — 一句话说明

## 关键争议与开放问题

- [ ] 问题描述 — 参考：[[questions]]

## 相关时间线

- [[timelines/...]] — 一句话说明
```

## 写作要求

- 只做导航入口，不展开具体对比表格或详细分析（这些属于 concept/analysis 页面）。
- 每个 [[链接]] 后附一句话说明，帮助读者判断是否需要深入。
- 概述段落不超过 3-5 句话。
- 当 concept/analysis 页面更新时，检查 overview 的链接和说明是否需要同步。
