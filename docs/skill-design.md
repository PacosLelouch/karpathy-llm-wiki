# Skill Design Notes

## 设计目标

`llm-wiki` 的目标是把 LLM 从一次性问答助手，升级为可维护 Markdown/Obsidian 知识库的长期维护者。

## 三层架构

### Skill 层（操作协议）

SKILL.md 瘦身为路由文档（约 100 行），包含：
- 触发场景和操作决策路由
- 目录结构概览
- Obsidian 写作规范
- 禁忌
- 自动化支持说明

五个操作的详细协议拆分为独立 references 文件，按需加载。这节省约 60% 的上下文 token：Query 操作只需加载 ~30 行的 query.md，而不是整个 276 行的 SKILL.md。

### Hook 层（硬约束自动执行）

| Hook | 作用 |
|------|------|
| `llm-wiki-raw-guard` | 阻止对 `raw/` 已有文件的修改（允许新建）。设 `LLM_WIKI_ALLOW_RAW_EDIT=1` 可临时放行 |
| `llm-wiki-post-write-indexer` | wiki/ 写入后提醒更新 index.md 和 log.md |

为什么需要 Hook：
- SKILL.md 中的"禁忌"依赖 Agent 自觉遵守，但实际执行中 Agent 可能遗忘或忽视
- Hook 将关键约束自动化执行，不占上下文 token
- `llm-wiki-raw-guard` 确保不修改 raw/，`llm-wiki-post-write-indexer` 确保索引不滞后

### Subagent 层（专项推理分析）

| Subagent | 作用 |
|----------|------|
| `llm-wiki-linter` | 语义性巡检分析，输出结构化巡检报告 |
| `llm-wiki-ingest-compiler` | 复杂摄入编译：raw → wiki 页面 → cascade updates → index/log 更新 |

为什么需要 Subagent：
- 语义性 lint 和复杂摄入编译需要深度分析，不适合全部写在 SKILL.md 中
- 按需调用，不常驻上下文，节省 token
- 专注单一职责，输出更结构化

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

普通查询不写文件，避免知识库被闲聊污染。只有用户明确要求保存、沉淀、归档或更新 wiki 时才写入。`llm-wiki-raw-guard` Hook 进一步确保 raw/ 不可修改（设 `LLM_WIKI_ALLOW_RAW_EDIT=1` 可临时放行）。

### Archive 是时间点快照

`mode: archive` 页面不参与后续 cascade updates。新来源推翻旧结论时，维护型页面应更新；归档页只在 lint 中报告可能过期。

### Lint 权限分级

确定性问题可自动修复；语义性判断只报告，避免 LLM 过度修改知识库。`llm-wiki-linter` Subagent 专门处理语义性巡检。

## 多平台生成策略

参照 ConvergentEngineerLoop 的 `_shared/` + `sync-platforms.py` 模式：

- 所有内容在 `_shared/` 维护（唯一真源）
- `sync-platforms.py` 一键生成 CodeBuddy/Codex/ClaudeCode 三平台文件
- 生成后各平台目录运行时零跨目录依赖
- 格式差异由脚本处理：CodeBuddy/Claude 使用 Markdown+YAML agents；Codex 使用 TOML agents
