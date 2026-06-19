# 问答归档模板

用于用户明确要求"保存、沉淀、归档、写入 wiki"的回答。归档页是时间点快照，默认不参与后续 cascade update。

```markdown
---
title: 归档标题
type: archive
mode: archive
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
archived: YYYY-MM-DD
question: 原始问题
sources: []
tags: []
status: active
evidence_level: synthesized
---

# 归档标题

> [!info] Archive
> 这是一次问答/分析的时间点快照。后续新资料进入 wiki 时，不会自动改写本页；如依据页面发生重大变化，应在巡检中报告。

## 原始问题

...

## 结论摘要

...

## 依据页面

- [[concepts/...]]
- [[entities/...]]
- [[analyses/...]]

## 归档内容

将对话回答轻度整理为适合 wiki 阅读的内容。

## 不确定性

- ...

## 后续问题

- [ ] ...
```
