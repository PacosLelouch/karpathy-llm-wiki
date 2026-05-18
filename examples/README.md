# LLM Wiki 示例

这些示例展示如何在 CodeBuddy 与 Obsidian 中使用 `llm-wiki` skill。

| 文件 | 展示内容 |
|---|---|
| `raw-source-example.md` | raw 原始资料采集格式 |
| `source-page-example.md` | 从 raw 编译出的来源摘要页 |
| `concept-page-example.md` | 跨来源概念综合页、证据等级、冲突标注 |
| `entity-page-example.md` | 实体页、关系和待研究问题 |
| `analysis-page-example.md` | 维护型分析页、比较表和当前建议 |
| `archive-page-example.md` | 显式归档的问答快照 |
| `index-example.md` | `wiki/index.md` 的类型/topic 混合索引 |
| `log-example.md` | ingest/query/archive/lint/repo 日志 |

## CodeBuddy 口令示例

```text
请使用 llm-wiki skill，摄入 raw/sources/2026-05-18-map-generator-notes.md。
```

```text
请使用 llm-wiki skill，基于当前 wiki 比较 WFC 和 BSP 的地图生成适用场景；只读回答，不修改文件。
```

```text
请使用 llm-wiki skill，把刚才的比较归档到 wiki/analyses，并更新 index.md 和 log.md。
```

```text
请使用 llm-wiki skill，对 wiki 做 lint。确定性问题自动修复，语义性问题只报告。
```
