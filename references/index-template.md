# `wiki/index.md` 模板

`index.md` 是内容地图，不替代全文搜索。它应帮助 LLM 和人类快速定位页面。

```markdown
# Index

## Overview

- [[overview]] — 当前整体综合理解。
- [[questions]] — 待研究问题与资料缺口。

## By Type

### Sources

| Page | Summary | Topic | Updated | Status |
|---|---|---|---|---|
| [[sources/source-title]] | 一句话摘要 | topic | YYYY-MM-DD | active |

### Entities

| Page | Summary | Topic | Updated | Status |
|---|---|---|---|---|
| [[entities/entity-name]] | 一句话摘要 | topic | YYYY-MM-DD | active |

### Concepts

| Page | Summary | Topic | Updated | Status |
|---|---|---|---|---|
| [[concepts/concept-name]] | 一句话摘要 | topic | YYYY-MM-DD | active |

### Analyses & Archives

| Page | Summary | Mode | Topic | Updated | Status |
|---|---|---|---|---|---|
| [[analyses/analysis-title]] | 一句话摘要 | maintained | topic | YYYY-MM-DD | active |
| [[analyses/archive-title]] | [Archived] 一句话摘要 | archive | topic | YYYY-MM-DD | active |

## By Topic

### topic-name

- [[concepts/...]] — ...
- [[entities/...]] — ...
- [[analyses/...]] — ...
```

## 维护规则

- Ingest、Archive、Lint 自动修复后必须更新。
- 普通 Query 不更新。
- 页面缺摘要时可临时写 `(no summary)`，后续再补。
- 指向不存在页面时标记 `[MISSING]`，不要直接删除。
