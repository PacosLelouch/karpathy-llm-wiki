# Archive 操作协议

Archive 只在用户明确要求时执行，用于保存一次问答、比较、结论或决策的时间点快照。

## 规则

- 默认保存到 `wiki/analyses/`，frontmatter 使用 `type: archive` 或 `type: analysis` + `mode: archive`。
- Archive 是 point-in-time snapshot，不参与后续 Cascade Updates。
- Archive 页面引用的是本次回答依据的 wiki 页面，不直接把 raw 作为主要来源，除非回答确实直接读取了 raw。
- 归档页文件名反映问题主题，而不是聊天日期本身。
- 更新 `wiki/index.md`，摘要前可标记 `[Archived]`。
- 追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] archive | 页面标题
- Question: ...
- Created: `wiki/analyses/...`
- Sources: `wiki/concepts/...`, `wiki/entities/...`
- Snapshot note: point-in-time archive; not cascade-updated.
```

模板见 `references/archive-template.md`。

## Archive 页面模板

```markdown
---
title: 页面标题
type: archive
mode: archive
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - wiki/concepts/...
  - wiki/entities/...
tags: []
status: active
evidence_level: synthesized
---

# 页面标题

> [!note] 归档快照
> 本页面为时间点归档，不参与后续自动更新。如引用的来源发生重大变化，将在巡检中报告。

## 原始问题

...

## 回答

...

## 依据

- `wiki/concepts/...`：...
- `wiki/entities/...`：...
```
