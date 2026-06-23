# LLM Wiki Skill 设计背景

## 核心理念

把 LLM Wiki 视为由 LLM 持续维护的 Markdown/Obsidian 知识库，而不是一次性 RAG 检索结果。人类选择资料、提出问题和判断方向；LLM 负责把资料编译为可链接、可追踪、可持续更新的 wiki 页面。

与一次性 RAG 的根本区别：知识综合发生在摄入和维护阶段，而非查询时。这让知识页面、索引、日志和交叉引用随时间复利增长。

## 三层架构

| 层 | 功能 | 执行方式 |
|---|---|---|
| **Skill** | 操作性协议、参考文件、模板、清单 | Agent 读取 SKILL.md 后按协议选择参考文件 |
| **Hook** | 硬约束自动执行 | 平台在特定事件时自动调用 |
| **Subagent** | 专项推理分析 | Agent 需要深度分析时调用 |

### 为什么需要 Hook？

- SKILL.md 中的"禁忌"依赖 Agent 自觉遵守，但实际执行中 Agent 可能遗忘或忽视
- Hook 将关键约束自动化执行：`raw-immutability-guard` 确保不修改 raw/，`post-write-indexer` 确保索引不滞后
- Hook 不占上下文 token，自动执行

### 为什么需要 Subagent？

- 语义性 lint 和复杂摄入编译需要深度分析，不适合全部写在 SKILL.md 中
- Subagent 按需调用，不常驻上下文，节省 token
- 专注单一职责，输出严格 YAML 结构化方案，主 agent 可直接遍历执行
- 简单操作（单来源摄入、确定性巡检）由主 agent 直接处理，无需 subagent
- `references/*.md` 是主 agent 协议，`agents/instructions/*.md` 是 subagent 协议，两者零重复

## Token 节省策略

原始 SKILL.md 约 276 行，每次触发全量加载。重构后：

- SKILL.md 瘦身至约 100 行（路由文档 + 概览 + 禁忌）
- 五个操作协议拆分为独立 reference，按需加载
- 典型场景节省约 60% token：
  - Query 操作只需加载 ~30 行的 query.md
  - Ingest 操作加载 ~80 行的 ingest.md
  - 只有 Schema/Repo 操作才需要加载更多参考

## 目录结构设计原则

- `raw/` 不可变：保存原始资料和采集元数据，不做任何观点改写
- `wiki/` 可变但可追踪：通过 index.md、log.md 和 frontmatter 追踪所有变更
- 主题分组通过 frontmatter `topic` 字段和 index.md 实现，不使用深层目录嵌套
- Obsidian 原生支持：双链、Properties、Bases、Canvas、Dataview
