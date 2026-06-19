# `wiki/log.md` 模板

`log.md` 是追加式操作日志，便于追踪知识库如何演化。

```markdown
# Log

## [YYYY-MM-DD] ingest | 来源标题或主题
- Raw source: `raw/sources/...`
- Created: `wiki/sources/...`
- Updated: `wiki/concepts/...`, `wiki/entities/...`, `wiki/analyses/...`
- Cascade updates: ...
- Conflicts / changes: ...
- Follow-up questions: ...

## [YYYY-MM-DD] query | 问题摘要
- Question: ...
- Read: `wiki/index.md`, `wiki/concepts/...`
- Written: none
- Key answer: ...

## [YYYY-MM-DD] archive | 页面标题
- Question: ...
- Created: `wiki/analyses/...`
- Sources: `wiki/concepts/...`, `wiki/entities/...`
- Snapshot note: point-in-time archive; not cascade-updated.

## [YYYY-MM-DD] lint | 范围
- Issues found: ...
- Auto-fixed: ...
- Report-only: ...
- Remaining: ...

## [YYYY-MM-DD] repo | 操作摘要
- Changed: `SKILL.md`, `references/...`, `examples/...`
- Validation: ...
```

## 规则

- 追加新条目，不重写历史。
- 日期使用当天日期。
- 普通只读 Query 可不写日志；如果用户要求记录查询，则写 `Written: none`。
