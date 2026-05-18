---
name: llm-wiki
description: "This skill should be used when creating, maintaining, querying, archiving, or linting an LLM-maintained Markdown/Obsidian wiki. 适用于资料摄入、raw/wiki/schema 分层、index/log 维护、双链、frontmatter、问答归档、知识库巡检、CodeBuddy skill 仓库化。"
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
- 将当前 skill 整理为可复用 CodeBuddy Agent Skill 仓库。

## 操作决策

优先按用户意图选择一个主操作：

1. **Initialize**：用户要求初始化知识库，或首次 Ingest 发现缺少基础结构。
2. **Ingest**：用户要求摄入、整理、归档资料，或提供 URL/文件/文本作为新来源。
3. **Query**：用户只是提问、总结、比较或要求“基于当前 wiki 回答”。
4. **Archive**：用户明确要求“保存、沉淀、归档、写入 wiki、生成分析页”。
5. **Lint**：用户要求检查、清理、补链、修复、巡检或发现知识库质量问题。
6. **Schema/Repo**：用户要求修改 skill、schema、模板、示例、README 或做成仓库。

重要写入边界：普通 Query 默认只读，不修改文件；只有 Ingest、Archive、Lint 自动修复、Schema/Repo 或用户明确要求写入时，才修改文件。

## 推荐目录结构

默认适配 Obsidian 与研究型知识库，保留类型目录：

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

## Initialize

仅在用户明确要求初始化，或首次 Ingest 发现基础结构缺失时执行。

步骤：

1. 检查 `raw/`、`wiki/`、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 是否存在。
2. 只创建缺失项，不覆盖已有文件。
3. 创建类型目录：`wiki/sources/`、`wiki/entities/`、`wiki/concepts/`、`wiki/analyses/`、`wiki/timelines/`。
4. 创建 `wiki/questions.md`。
5. 如用户要求，基于 `references/wiki-schema-template.md` 生成或更新项目级 `AGENTS.md`。
6. 追加 `wiki/log.md`：`## [YYYY-MM-DD] repo | Initialize wiki structure`。

如果 Query 或 Lint 找不到 wiki 结构，不要自动初始化；告知用户先运行 Ingest 或明确要求初始化。

## Ingest

Ingest = 获取/确认原始资料 + 编译进 wiki + 联动更新 + 更新索引与日志。

### 1. 读取既有上下文

1. 先读 `wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 和明显相关页面。
2. 搜索是否已有相同来源、同名概念、同一实体或相近分析页。
3. 不凭聊天记忆补事实；事实回到 `raw/` 或已有 wiki 页面验证。

### 2. 处理 raw 来源

- 如果来源已经在 `raw/`：保持原文件不变，只读取。
- 如果用户提供 URL、粘贴文本或外部文件，并明确要求摄入：保存为 `raw/sources/YYYY-MM-DD-short-slug.md` 或领域子路径下的同名文件。
- 文件名使用小写英文、短横线、最多约 60 个字符；日期未知时可不带发布日期，但采集日期仍写入 metadata。
- raw 文件应忠实保存原意，可以清理导航栏、HTML 噪声、重复空白，但不要改写观点。
- 图片、PDF、截图等附件放入 `raw/assets/`，并在 raw/source 页面记录路径。

raw 模板见 `references/raw-template.md`。

### 3. 编译 wiki 页面

根据内容归属选择一个或多个动作：

- 单个来源事实：创建或更新 `wiki/sources/` 来源摘要页。
- 新实体：创建 `wiki/entities/` 页面。
- 新概念：创建 `wiki/concepts/` 页面。
- 跨页面综合、比较、技术选型：创建或更新 `wiki/analyses/` 维护型分析页。
- 时间演进：更新 `wiki/timelines/`。
- 资料缺口：更新 `wiki/questions.md`。

判断规则：

- 同一核心概念已有页面：合并更新，不创建重复页。
- 新来源修正旧说法：保留旧说法来源，新增“争议、矛盾或版本变化”。
- 同一来源影响多个页面：逐一更新受影响页面。
- 页面 `updated` 日期只在知识内容发生变化时刷新。

### 4. Cascade Updates

主页面更新后，检查涟漪影响：

1. 同目录相关页面是否被新资料影响。
2. `wiki/index.md` 中相邻主题或相关条目是否需要更新摘要、状态或链接。
3. `wiki/overview.md` 是否需要更新全局综合理解。
4. `wiki/questions.md` 是否需要新增、关闭或调整问题。
5. 维护型 `analysis` 是否被新证据影响。
6. `mode: archive` 的页面不自动改写；若其引用内容明显过期，只在巡检中报告或标记。

### 5. Post-Ingest

1. 更新 `wiki/index.md`：新增/更新所有被触达页面的链接、摘要、类型、topic、状态、更新时间、来源数。
2. 追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] ingest | 来源标题或主题
- Raw source: `raw/sources/...`
- Created: `wiki/sources/...`
- Updated: `wiki/concepts/...`, `wiki/entities/...`, `wiki/analyses/...`
- Cascade updates: ...
- Conflicts / changes: ...
- Follow-up questions: ...
```

## Query

Query 默认只读。

步骤：

1. 先读 `wiki/index.md` 定位相关页面。
2. 再读相关 `sources`、`entities`、`concepts`、`analyses`、`overview`、`questions` 页面。
3. 优先使用 wiki 中已经沉淀的内容，而不是模型训练知识。
4. 回答中标明依据页面或来源；对话中使用项目相对路径，例如 `wiki/concepts/perlin-noise.md`。
5. 明确说明不确定性、证据不足、冲突和待验证点。
6. 不写入任何文件，除非用户明确要求保存、沉淀、归档或更新 wiki。

如果回答有长期价值但用户没有要求写入，可以在结尾简短建议：“这个回答适合归档为分析页，如需我可以保存。”

## Archive

Archive 只在用户明确要求时执行，用于保存一次问答、比较、结论或决策的时间点快照。

规则：

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

## Lint

Lint 分为“确定性自动修复”和“语义性只报告”。

### 可自动修复

仅修复可验证、低风险的问题：

- `wiki/index.md` 漏掉实际存在的 wiki 页面：补条目，摘要可用 `(no summary)` 占位。
- `wiki/index.md` 指向不存在页面：标记 `[MISSING]`，不要直接删除条目。
- wiki 内部链接目标不存在，但能唯一定位到同名文件：修正链接。
- frontmatter 缺少稳定字段：在不改变正文含义的前提下补字段。
- `status`、`type`、`updated` 等字段格式明显不一致：规范化。
- `log.md` 缺少本次 lint 记录：追加记录。

### 只报告，不自动修复

以下依赖语义判断，默认只报告：

- 事实矛盾、来源冲突、过期观点。
- 页面是否应合并、拆分、重命名或废弃。
- 概念定义是否准确。
- 重要概念/实体是否缺页。
- 孤立页面是否真的无价值。
- `mode: archive` 页面引用的来源后来发生重大变化。
- 证据等级是否需要人工调整。

### Post-Lint

追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] lint | 范围
- Issues found: ...
- Auto-fixed: ...
- Report-only: ...
- Remaining: ...
```

详细清单见 `references/lint-checklist.md`。

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

## CodeBuddy 使用规范

- 执行具体任务前，先读取本 skill 和相关 `references/` 模板。
- 用户说“按规范”时，先读取项目级 `AGENTS.md`、`CLAUDE.md` 或其他 schema。
- 对复杂 wiki 修改使用任务清单；普通查询不创建不必要文件。
- 修改 skill 本身时，可使用 `skill-creator` 校验结构。
- 如果产出可查看文档，完成后打开主结果文件供用户审阅。

## 仓库化规范

当用户要求把本 skill 做成仓库：

1. 保持最小可复用结构：`SKILL.md`、`README.md`、`LICENSE`、`.gitignore`、`references/`、`examples/`。
2. 不把本地绝对路径写入通用 README。
3. README 应包含：定位、安装/复制方式、快速开始、操作协议、Obsidian 配合方式、CodeBuddy 触发口令、与 RAG 的区别、示例说明。
4. examples 应覆盖 raw、source、concept、entity、analysis、archive、index、log。
5. 用 skill 校验脚本验证 `SKILL.md` 元数据和目录结构。

## 禁忌

- 不修改 `raw/` 原始资料，除非用户明确要求整理文件名或移动位置。
- 不在普通 Query 中写文件。
- 不把新来源只写成孤立摘要而不更新相关知识页。
- 不在存在矛盾时静默覆盖旧结论；必须保留来源和冲突说明。
- 不凭聊天记忆补事实。
- 不让 `index.md` 和 `log.md` 滞后于实际页面变更。
- 不把语义性判断伪装成确定性自动修复。
