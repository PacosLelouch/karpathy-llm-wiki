# Skill Design Notes

## 设计目标

`llm-wiki` 的目标是把 LLM 从一次性问答助手，升级为可维护 Markdown/Obsidian 知识库的长期维护者。

## 核心取舍

### 保留类型目录

不采用单层 `wiki/<topic>/<article>.md` 结构，而是保留：

- `wiki/sources/`
- `wiki/entities/`
- `wiki/concepts/`
- `wiki/analyses/`
- `wiki/timelines/`

原因：该结构更适合 Obsidian、研究型知识库和实体/概念/分析分层。

### 用 frontmatter 表达主题维度

主题不通过深层目录表达，而通过：

```yaml
topic: [terrain-generation, pcg]
```

再由 `index.md`、Bases、Canvas 或 Dataview 组织视图。

### Query 默认只读

普通查询不写文件，避免知识库被闲聊污染。只有用户明确要求保存、沉淀、归档或更新 wiki 时才写入。

### Archive 是时间点快照

`mode: archive` 页面不参与后续 cascade updates。新来源推翻旧结论时，维护型页面应更新；归档页只在 lint 中报告可能过期。

### Lint 权限分级

确定性问题可自动修复；语义性判断只报告，避免 LLM 过度修改知识库。
