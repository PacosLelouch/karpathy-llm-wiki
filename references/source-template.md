# 来源页模板

用于 `wiki/sources/`，把单个 raw 来源编译成摘要页。

```markdown
---
title: 来源标题
type: source
date: YYYY-MM-DD 或 Unknown
ingested: YYYY-MM-DD
author: 作者或机构
source_path: raw/sources/...
raw:
  - raw/sources/...
topic: []
tags: []
status: active
evidence_level: primary
---

# 来源标题

## 摘要

一段话说明该来源讨论什么、为何重要、和当前 wiki 的关系。

## 关键要点

- 要点。来源位置：段落/章节/页码。

## 关键证据/引用

- “原文短引文。” — 位置说明

## 涉及实体

- [[entities/...]] — 关系说明

## 涉及概念

- [[concepts/...]] — 关系说明

## 对既有 wiki 的影响

- 支持：...
- 修正：...
- 冲突：...
- 新增：...

## 待验证问题

- [ ] ...
```

## 写作要求

- 来源页仍然是摘要，不要替代 raw 原文。
- 所有事实性强的要点尽量标注位置或来源片段。
- 发现冲突时，不覆盖旧说法，记录差异和各自来源。
