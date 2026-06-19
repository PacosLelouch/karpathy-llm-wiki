# Initialize 操作协议

仅在用户明确要求初始化，或首次 Ingest 发现基础结构缺失时执行。

## 步骤

1. 检查 `raw/`、`wiki/`、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 是否存在。
2. 只创建缺失项，不覆盖已有文件。
3. 创建类型目录：`wiki/sources/`、`wiki/entities/`、`wiki/concepts/`、`wiki/analyses/`、`wiki/timelines/`。
4. 创建 `wiki/questions.md`。
5. 如用户要求，基于 `references/wiki-schema-template.md` 生成或更新项目级 `AGENTS.md`。
6. 追加 `wiki/log.md`：`## [YYYY-MM-DD] repo | Initialize wiki structure`。

## 注意

- 如果 Query 或 Lint 找不到 wiki 结构，不要自动初始化；告知用户先运行 Ingest 或明确要求初始化。
- 初始化后应告知用户接下来可以摄入资料或设置 wiki schema。

## 初始文件内容模板

### wiki/index.md

```markdown
---
title: 内容索引
type: index
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 内容索引

## 来源摘要

## 实体

## 概念

## 分析

## 时间线
```

### wiki/log.md

```markdown
---
title: 操作日志
type: log
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 操作日志
```

### wiki/overview.md

```markdown
---
title: 全局概览
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
---

# 全局概览

> 尚未建立综合理解。随着资料摄入，此页面将逐步更新。
```

### wiki/questions.md

```markdown
---
title: 待研究问题
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
---

# 待研究问题

> 随着知识库建设，已解决的问题将被移除，新问题将被添加。
```
