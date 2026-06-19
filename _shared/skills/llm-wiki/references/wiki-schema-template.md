# LLM Wiki Schema 总纲模板

用于创建或重构由 LLM 增量维护的 Obsidian/Markdown wiki。按领域裁剪，不必全部照搬。

## 三层结构

- `raw/`：不可变事实来源，保存原文、附件和采集元数据。
- `wiki/`：LLM 维护的结构化知识层，保存来源摘要、实体、概念、分析、时间线和问题。
- schema：`SKILL.md`、`AGENTS.md`、`CLAUDE.md` 等操作协议，约束目录、命名、模板、写入边界和巡检规则。

## 推荐目录

```text
raw/
  sources/
  assets/
wiki/
  index.md
  log.md
  overview.md
  sources/
  entities/
  concepts/
  analyses/
  timelines/
  questions.md
```

## 页面类型

| 类型 | 路径 | 用途 | 模板 |
|---|---|---|---|
| raw | `raw/sources/` | 原始资料 | `raw-template.md` |
| source | `wiki/sources/` | 来源摘要 | `source-template.md` |
| entity | `wiki/entities/` | 实体综合页 | `entity-template.md` |
| concept | `wiki/concepts/` | 概念综合页 | `concept-template.md` |
| analysis | `wiki/analyses/` | 维护型分析 | `analysis-template.md` |
| archive | `wiki/analyses/` | 问答快照 | `archive-template.md` |
| index | `wiki/index.md` | 内容地图 | `index-template.md` |
| log | `wiki/log.md` | 操作日志 | `log-template.md` |

## 稳定 frontmatter 字段

```yaml
title: 页面标题
type: source | entity | concept | analysis | archive | timeline
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
raw: []
tags: []
status: stub | active | mature | outdated | conflicting
evidence_level: primary | secondary | synthesized | speculative
mode: maintained | archive
```

字段说明：

- `type`：页面类别。
- `topic`：跨目录主题标签，用于 Obsidian Bases、Dataview 和 `index.md` 分组。
- `status`：页面成熟度或健康状态。
- `evidence_level`：证据等级。
- `mode`：`maintained` 表示会持续更新；`archive` 表示时间点快照。

## 工作流总览

1. Initialize：只创建缺失结构，不覆盖已有文件。
2. Ingest：确认/采集 raw，编译 source/entity/concept/analysis，做 cascade updates，更新 index/log。
3. Query：默认只读，回答中引用 wiki 页面和不确定性。
4. Archive：仅在用户明确要求时把问答保存为快照。
5. Lint：确定性问题可自动修复；语义性问题只报告。

## 必读参考

- Obsidian 写作：`obsidian-style-guide.md`
- 使用规范：`usage-guide.md`
- 巡检清单：`lint-checklist.md`
- 日志格式：`log-template.md`

## 可选 Obsidian 视图

- Bases 视图模板：`bases-template.base`
- Canvas 知识地图模板：`knowledge-map-template.canvas`
