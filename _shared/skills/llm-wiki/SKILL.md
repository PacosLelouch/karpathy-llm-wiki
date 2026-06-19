---
name: llm-wiki
description: "This skill should be used when creating, maintaining, querying, archiving, or linting an LLM-maintained Markdown/Obsidian wiki. 适用于资料摄入、raw/wiki/schema 分层、index/log 维护、双链、frontmatter、问答归档、知识库巡检。"
---

# LLM Wiki

## 概览

把 LLM Wiki 视为由 LLM 持续维护的 Markdown/Obsidian 知识库，而不是一次性 RAG 检索结果。人类选择资料、提出问题和判断方向；LLM 负责把资料编译为可链接、可追踪、可持续更新的 wiki 页面。

核心思想：

- `raw/` 是不可变证据层：保存原始资料、附件和采集元数据。
- `wiki/` 是结构化知识层：保存来源摘要、实体、概念、分析、时间线和开放问题。
- `SKILL.md`、`AGENTS.md`、`CLAUDE.md` 等 schema 是操作协议层：规定目录、模板、写入边界和质量标准。

## 触发场景

当用户提出以下任务时使用本 skill：

- 创建或重构个人/团队/研究/读书/业务/竞品/课程/项目知识库。
- 摄入 URL、论文、文章、会议纪要、截图、PDF、Markdown、代码仓库说明或粘贴文本。
- 基于现有 wiki 回答问题、比较方案、总结主题、生成研究结论。
- 将明确要求保存的问答归档为 wiki 页面。
- 巡检 `index.md`、`log.md`、frontmatter、双链、断链、孤立页、矛盾、过期内容和资料缺口。
- 设计或优化 Obsidian Markdown wiki 的 schema、模板、Bases、Canvas、Dataview 友好字段。
- 将当前 skill 整理为可复用仓库（参见 `references/usage-guide.md`）。

## 操作决策

优先按用户意图选择一个主操作，然后读取对应的参考文件获取详细协议：

| 操作 | 触发信号 | 参考文件 | 写入行为 |
|------|---------|---------|---------|
| **Initialize** | 初始化知识库，或首次 Ingest 缺结构 | `references/initialize.md` | 只创建缺失结构，不覆盖已有文件 |
| **Ingest** | 摄入/整理/归档资料，提供 URL/文件/文本 | `references/ingest.md` | 更新 raw/wiki/index/log |
| **Query** | 提问/总结/比较/基于 wiki 回答 | `references/query.md` | 默认只读，不写文件 |
| **Archive** | 明确要求保存/沉淀/归档/写入 wiki | `references/archive.md` | 新建归档页，更新 index/log |
| **Lint** | 检查/清理/补链/巡检/健康检查 | `references/lint.md` | 确定性可自动修复，语义性只报告 |

额外操作：
- **Schema/Repo**：用户要求修改 skill、schema、模板、示例、README 或做成仓库。读取 `references/usage-guide.md` 和 `references/wiki-schema-template.md`。

重要写入边界：普通 Query 默认只读，不修改文件；只有 Ingest、Archive、Lint 自动修复、Schema/Repo 或用户明确要求写入时，才修改文件。

## 推荐目录结构

```text
raw/                         # 原始资料，不修改
  sources/                   # 文章、论文、网页剪藏、转录稿、代码仓库 README
  assets/                    # 图片、附件、PDF、截图、音视频、示意图
wiki/                        # LLM 维护的知识层
  index.md                   # 内容索引
  log.md                     # 追加式操作日志
  overview.md                # 全局概览 / 当前综合理解
  sources/                   # 每个来源的摘要页
  entities/                  # 人物、组织、项目、工具、算法、游戏等实体
  concepts/                  # 概念、理论、机制、技术、主题
  analyses/                  # 维护型分析页与显式归档页
  timelines/                 # 时间线，可选
  questions.md               # 待研究问题 / 资料缺口
AGENTS.md 或 CLAUDE.md        # 项目级 wiki schema，可选但推荐
```

不要无故改成 `wiki/<topic>/<article>.md`。如果需要主题视角，用 frontmatter 的 `topic` 字段、`index.md` 分组、Obsidian Bases 或 Canvas 表达。

## Obsidian 写作规范

- wiki 内部语义链接优先使用 Obsidian 双链：`[[concepts/perlin-noise]]`。
- 对话回答和 README 中引用文件时使用项目相对路径：`wiki/concepts/perlin-noise.md`。
- 图片和附件使用相对路径或 Obsidian embed：`![[../raw/assets/diagram.png]]`。
- 使用 YAML frontmatter 支持 Obsidian Properties、Bases、Dataview 和后续自动巡检。
- 可使用 callout 标注证据、警告和待验证项：`> [!note]`、`> [!warning]`、`> [!question]`。
- 避免同一实体/概念重复建页；先查 `index.md` 和现有文件。

建议稳定 frontmatter 字段：

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

详细 frontmatter 和 Obsidian 规范见 `references/obsidian-style-guide.md`。

## 自动化支持

本技能提供 Hook 和 Subagent 两个自动化层，与 Skill 协同工作：

### Hook（硬约束自动执行）

| Hook | 触发时机 | 作用 |
|------|---------|------|
| `llm-wiki-raw-guard` | 文件修改前 | 阻止对 `raw/` 目录已有文件的修改（允许新建） |
| `llm-wiki-post-write-indexer` | 文件修改后 | wiki/ 下非 index/log 文件被修改时，提醒更新索引和日志 |

Hook 配置在平台设置文件中注册，Agent 无法跳过。

### Subagent（专项推理分析）

| Subagent | 适用场景 | 作用 |
|----------|---------|------|
| `llm-wiki-linter` | 执行 Lint 操作时 | 语义性巡检分析，输出结构化巡检报告 |
| `llm-wiki-ingest-compiler` | 执行 Ingest 操作时 | 处理复杂编译逻辑：raw → wiki 页面 → cascade updates → index/log 更新 |

## 禁忌

- 不修改 `raw/` 原始资料，除非用户明确要求整理文件名或移动位置。
- 不在普通 Query 中写文件。
- 不把新来源只写成孤立摘要而不更新相关知识页。
- 不在存在矛盾时静默覆盖旧结论；必须保留来源和冲突说明。
- 不凭聊天记忆补事实。
- 不让 `index.md` 和 `log.md` 滞后于实际页面变更。
- 不把语义性判断伪装成确定性自动修复。
