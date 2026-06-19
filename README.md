# llm-wiki

一个面向多平台 AI 编码助手的 LLM Wiki skill，用于创建、维护、查询、归档和巡检由 LLM 增量维护的 Obsidian/Markdown 知识库。

它吸收 Karpathy LLM Wiki 的核心思想：让 LLM 编写和维护 wiki，人类负责选择资料、提出问题和判断方向。与一次性 RAG 不同，LLM Wiki 会在资料摄入和维护阶段持续编译知识，让知识页面、索引、日志和交叉引用随时间复利增长。

## 前置条件

- **Python 3.8+**：Hook 脚本用 Python 编写，需要系统 PATH 中有 `python` 命令
  - Windows：安装 [Python](https://www.python.org/downloads/) 时勾选 "Add Python to PATH"
  - macOS/Linux：`python3 --version` 可用时，可创建软链接 `sudo ln -s $(which python3) /usr/local/bin/python`
  - 验证：在终端运行 `python --version`，应输出 Python 3.8+
- **PyYAML**：sync 脚本依赖 `yaml` 模块，运行 `pip install pyyaml` 安装
- **Git Bash**（仅 Windows + CodeBuddy 用户）：在 CodeBuddy 设置 → Hooks → 高级设置中，将执行器配置为 `C:\Program Files\Git\bin\bash.exe`

## 三层架构

| 层 | 功能 | 执行方式 |
|---|---|---|
| **Skill** | 操作性协议、参考文件、模板、清单 | Agent 读取 SKILL.md 后按协议选择参考文件 |
| **Hook** | 硬约束自动执行 | 平台在特定事件时自动调用 |
| **Subagent** | 专项推理分析 | Agent 需要深度分析时调用 |

三层协同工作流程：

```
用户描述任务
  ↓
┌─── Skill 层 ────────────────────────────────────┐
│ Agent 读取 SKILL.md，按协议选择操作和参考文件      │
│ Initialize / Ingest / Query / Archive / Lint      │
└──────────────────────────────────────────────────┘
  ↓
┌─── Hook 层 ─────────────────────────────────────┐
│ 修改前：llm-wiki-raw-guard 阻止修改 raw/     │
│ 修改后：llm-wiki-post-write-indexer 提醒更新 index/log    │
└──────────────────────────────────────────────────┘
  ↓
┌─── Subagent 层 ─────────────────────────────────┐
│ llm-wiki-linter       语义性巡检分析                  │
│ llm-wiki-ingest-compiler   复杂摄入编译与级联更新          │
└──────────────────────────────────────────────────┘
```

### Hook 列表

| Hook | 触发时机 | 作用 | 拦截方式 |
|------|---------|------|---------|
| `llm-wiki-raw-guard` | 文件修改前 | 阻止对 `raw/` 目录已有文件的修改（允许新建） | deny（阻止修改） |
| `llm-wiki-post-write-indexer` | 文件修改后 | wiki/ 下非 index/log 文件被修改时，提醒更新索引和日志 | additionalContext（不阻止） |

### Subagent 列表

| Subagent | 适用场景 | 作用 |
|----------|---------|------|
| `llm-wiki-linter` | 执行 Lint 操作时 | 语义性巡检分析，输出结构化巡检报告 |
| `llm-wiki-ingest-compiler` | 执行 Ingest 操作时 | 处理复杂编译逻辑：raw → wiki 页面 → cascade updates → index/log 更新 |

## 适合什么场景

- 个人/团队知识库
- 论文、文章、会议纪要、代码仓库 README、网页剪藏摄入
- Obsidian 双链、frontmatter、Bases、Canvas 管理
- 基于 wiki 的问答、比较、总结和分析
- 问答结果显式归档
- `index.md`、`log.md`、断链、孤立页、冲突、过期内容巡检
- 为项目生成 `AGENTS.md` / `CLAUDE.md` wiki schema

## 五个核心操作

| 操作 | 触发 | 写入行为 |
|---|---|---|
| Initialize | 初始化 wiki 或首次摄入缺结构 | 只创建缺失结构，不覆盖已有文件 |
| Ingest | 摄入 URL/文件/文本/raw 来源 | 更新 raw/wiki/index/log |
| Query | 基于当前 wiki 提问 | 默认只读，不写文件 |
| Archive | 明确要求保存/沉淀/归档 | 新建归档页，更新 index/log |
| Lint | 巡检/修复/补链/健康检查 | 确定性问题可自动修复，语义问题只报告 |

## 系统生成方式

本项目采用 `_shared/` 真源 + `sync-platforms.py` 一键生成的模式。所有内容在 `_shared/` 中维护，通过脚本自动生成三个平台的独立可用包。

### 生成文件夹包

文件夹包是最直接的安装方式，将平台对应的目录复制到项目根目录即可：

```bash
python scripts/sync-platforms.py --format folders
```

生成结果：

```
CodeBuddy/                  # CodeBuddy 文件夹包
└── .codebuddy/
    ├── hooks/              # Hook 脚本 + llm_wiki_hook_utils.py（CodeBuddy 版）
    ├── agents/             # Markdown + YAML 格式
    ├── skills/llm-wiki/    # SKILL.md + references/
    └── settings.json       # Hook 配置

Codex/                      # Codex 文件夹包
├── .codex/
│   ├── hooks/              # Hook 脚本 + llm_wiki_hook_utils.py（Codex 版）
│   ├── agents/             # TOML 格式
│   └── config.toml         # Agent + Hook 配置
└── .agents/
    └── skills/llm-wiki/    # SKILL.md + references/

ClaudeCode/                 # Claude Code 文件夹包
└── .claude/
    ├── hooks/              # Hook 脚本 + llm_wiki_hook_utils.py（Claude 版）
    ├── agents/             # Markdown + YAML 格式
    ├── skills/llm-wiki/    # SKILL.md + references/
    └── settings.json       # Hook 配置
```

### 生成插件包

插件包是各平台的原生插件格式，适合通过包管理器安装：

```bash
python scripts/sync-platforms.py --format plugins
```

生成结果：

```
dist/
├── claude-llm-wiki-plugin/       # Claude Code 一体化插件
│   ├── .claude-plugin/plugin.json
│   ├── skills/llm-wiki/
│   ├── hooks/
│   ├── agents/
│   └── marketplace.json
├── codebuddy-llm-wiki-plugin/    # CodeBuddy Skills ZIP + 辅助配置
│   ├── llm-wiki.zip              # Skills ZIP（导入用）
│   ├── settings-hooks.json       # Hook 配置（需手动合并）
│   └── agents/                   # Agent 定义
└── codex-llm-wiki-plugin/        # Codex 文件夹包（无原生插件格式）
    ├── .codex/                   # 同文件夹包的 .codex/
    └── .agents/skills/llm-wiki/  # Skills
```

### 同时生成两种

```bash
python scripts/sync-platforms.py --format folders
python scripts/sync-platforms.py --format plugins
```

## 安装和使用

### 方式一：文件夹包安装

选择你的平台，将对应目录下的文件复制到项目根目录：

```bash
# CodeBuddy 用户
cp -r CodeBuddy/.codebuddy /path/to/your/project/

# Codex 用户
cp -r Codex/.codex /path/to/your/project/
cp -r Codex/.agents /path/to/your/project/

# Claude Code 用户
cp -r ClaudeCode/.claude /path/to/your/project/
```

### 方式二：插件包安装

先生成插件包：
```bash
python scripts/sync-platforms.py --format plugins
```

**Claude Code** — 一体化插件，安装后自动生效：
```
/plugin marketplace add ./dist/claude-llm-wiki-plugin
```

**CodeBuddy** — Skills ZIP 导入 + 手动配置：
1. 设置 → Skills → 导入 `dist/codebuddy-llm-wiki-plugin/llm-wiki.zip`
2. 将 `settings-hooks.json` 内容合并到 `.codebuddy/settings.json`
3. 将 `agents/` 复制到 `.codebuddy/agents/`

**Codex** — 复制文件夹包（无原生插件格式）：
```bash
cp -r dist/codex-llm-wiki-plugin/.codex /path/to/your/project/
cp -r dist/codex-llm-wiki-plugin/.agents /path/to/your/project/
```

## 使用示例

### 示例 1：初始化知识库

```
用户：请使用 llm-wiki skill，初始化当前项目的 wiki 结构，并生成 AGENTS.md。

Agent（读取 SKILL.md → 选择 Initialize 操作 → 加载 references/initialize.md）：
  → 创建 raw/、wiki/ 目录结构
  → 生成 wiki/index.md、wiki/log.md、wiki/overview.md
  → 生成 wiki/sources/、wiki/entities/、wiki/concepts/、wiki/analyses/
  → 生成 AGENTS.md（项目级 wiki schema）

Hook 作用：
  → llm-wiki-raw-guard：不触发（只创建新文件）
  → llm-wiki-post-write-indexer：提醒更新 index.md 和 log.md
```

### 示例 2：摄入资料

```
用户：请使用 llm-wiki skill，摄入 raw/sources/attention-is-all-you-need.md，
      并更新相关概念页、index.md 和 log.md。

Agent（选择 Ingest 操作 → 加载 references/ingest.md）：
  → 读取 raw/sources/attention-is-all-you-need.md
  → 编译为 wiki/sources/attention-is-all-you-need.md（来源摘要页）
  → 创建/更新 wiki/concepts/transformer-architecture.md
  → 创建/更新 wiki/concepts/self-attention.md
  → 创建/更新 wiki/entities/vaswani-et-al.md
  → 更新 wiki/index.md（添加新页面索引）
  → 更新 wiki/log.md（追加摄入记录）

Hook 作用：
  → llm-wiki-raw-guard：确认 raw/ 文件未被修改 ✅
  → llm-wiki-post-write-indexer：检测到 wiki/ 下文件变更，提醒确认 index.md 和 log.md 已更新

Subagent 作用（复杂摄入时自动调用）：
  → llm-wiki-ingest-compiler：处理 raw → wiki 编译逻辑，执行级联更新
```

### 示例 3：查询（只读）

```
用户：请使用 llm-wiki skill，基于当前 wiki 回答：Transformer 和 RNN 的核心区别是什么？
      这次只读，不要修改文件。

Agent（选择 Query 操作 → 加载 references/query.md）：
  → 读取 wiki/index.md 获取知识结构
  → 读取 wiki/concepts/transformer-architecture.md
  → 读取 wiki/concepts/rnn-sequence-modeling.md（如果存在）
  → 综合回答，给出双链引用：[[concepts/transformer-architecture]]、[[concepts/rnn-sequence-modeling]]
  → 不修改任何文件

Hook 作用：
  → llm-wiki-raw-guard：不触发（Query 只读）
  → llm-wiki-post-write-indexer：不触发（无文件修改）
```

### 示例 4：归档问答

```
用户：请使用 llm-wiki skill，把刚才的回答归档为 analysis 页面，
      并更新 index.md 和 log.md。

Agent（选择 Archive 操作 → 加载 references/archive.md）：
  → 创建 wiki/analyses/transformer-vs-rnn-comparison.md
  → 写入 frontmatter：type: analysis, sources: [...], status: active
  → 更新 wiki/index.md（添加分析页索引）
  → 更新 wiki/log.md（追加归档记录）

Hook 作用：
  → llm-wiki-raw-guard：不触发（不涉及 raw/）
  → llm-wiki-post-write-indexer：检测到 wiki/analyses/ 下新文件，提醒确认 index.md 和 log.md 已更新
```

### 示例 5：巡检与修复

```
用户：请使用 llm-wiki skill，对当前 wiki 做 lint。确定性问题可自动修复，语义性问题只报告。

Agent（选择 Lint 操作 → 加载 references/lint.md）：
  → 读取 wiki/index.md、wiki/log.md 和所有 wiki 页面
  → 检查 frontmatter 完整性 → 发现 2 个页面缺少 type 字段 → 自动修复
  → 检查双链有效性 → 发现 3 个断链 → 报告
  → 检查 index.md 覆盖率 → 发现 1 个页面未在 index 中 → 自动补充
  → 检查 log.md 时效性 → log 已滞后 2 次修改 → 自动追加
  → 检查孤立页 → 发现 1 个无入链页面 → 报告
  → 检查内容冲突 → 发现 2 个概念页存在矛盾描述 → 报告

Hook 作用：
  → llm-wiki-raw-guard：确认修复过程未触及 raw/ ✅
  → llm-wiki-post-write-indexer：修复后提醒确认 index.md 和 log.md 一致性

Subagent 作用：
  → llm-wiki-linter：执行语义性巡检分析（矛盾检测、内容质量评估）
```

### 示例 6：Hook 拦截保护

```
Agent 尝试修改 raw/sources/article.md（已有文件）：

llm-wiki-raw-guard 触发：
  → 检测到修改目标在 raw/ 目录下且文件已存在
  → 返回 deny，原因："raw/ 目录下的已有文件不可修改，只允许新建文件"
  → Agent 收到拒绝，改为只读取 raw 文件，将修改写入 wiki/ 层
```

## 项目结构

```text
llm-wiki/
  _shared/                    # 开发期真源（仅维护用，运行时不依赖）
    skills/llm-wiki/          # SKILL.md + references/ + README.md
    hooks/                    # 2 个 Hook 主脚本 + templates/（三平台 utils）
    agents/                   # 2 个 Agent 指令 + agents.yaml
    README.md                 # 各平台详细使用指南

  scripts/
    sync-platforms.py         # 真源 → 三平台生成脚本
    validate_repo.py          # 仓库校验脚本
    package_skill.ps1         # Windows 打包辅助

  examples/                   # 完整示例
  docs/                       # 仓库维护文档
  assets/                     # 预留资源目录

  CodeBuddy/                  # CodeBuddy 文件夹包（由 sync 生成，已加入 .gitignore）
  Codex/                      # Codex 文件夹包（由 sync 生成，已加入 .gitignore）
  ClaudeCode/                 # Claude Code 文件夹包（由 sync 生成，已加入 .gitignore）

  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  SECURITY.md
  CODE_OF_CONDUCT.md
  LICENSE
```

## Obsidian 支持

- 使用 `[[concepts/perlin-noise]]` 形式的双链。
- 使用 YAML frontmatter 支持 Properties、Bases、Dataview 和巡检。
- 使用 callout 标注来源、冲突、待验证问题和当前建议。
- 可选 Bases 视图模板和 Canvas 知识地图模板。

## 开发和维护

### 修改真源

所有内容维护在 `_shared/` 目录下。修改后运行 sync 生成三平台文件：

```bash
# 生成文件夹包
python scripts/sync-platforms.py --format folders

# 生成插件包
python scripts/sync-platforms.py --format plugins

# 同时生成两种
python scripts/sync-platforms.py --format folders
python scripts/sync-platforms.py --format plugins
```

### 修改什么、在哪里改

| 想改的内容 | 修改位置 | sync 后生效位置 |
|-----------|---------|---------------|
| 操作协议、触发、禁忌 | `_shared/skills/llm-wiki/SKILL.md` | 三平台 skills/ |
| 各操作详细协议 | `_shared/skills/llm-wiki/references/*.md` | 三平台 skills/references/ |
| 模板和示例 | `_shared/skills/llm-wiki/references/*-template.md` | 三平台 skills/references/ |
| Hook 检测逻辑 | `_shared/hooks/*.py`（主脚本） | 三平台 hooks/ |
| Hook 输出格式 | `_shared/hooks/templates/llm_wiki_hook_utils_*.py` | 对应平台 hooks/llm_wiki_hook_utils.py |
| Agent 指令 | `_shared/agents/instructions/*.md` | 三平台 agents/ |
| Agent 元数据 | `_shared/agents/agents.yaml` | 生成时读取 |

### 运行时独立性

删除 `_shared/` 和 `scripts/` 后，`CodeBuddy/`、`Codex/`、`ClaudeCode/` 三个目录仍可独立工作。每个目录拥有完整的 hooks、agents、skills、config，运行时零跨目录依赖。

## 本地校验

```bash
# 校验仓库结构
python -X utf8 scripts/validate_repo.py .

# 校验 SKILL.md（CodeBuddy 环境）
# 使用 skill-creator 的 quick_validate.py
```

## 故障排查

### Hook 未执行

1. **确认 Python 可用**：在终端运行 `python --version`，确保输出 Python 3.8+
2. **CodeBuddy Windows 用户**：在设置 → Hooks → 高级设置中配置执行器为 Git Bash（如 `C:\Program Files\Git\bin\bash.exe`）
3. **确认 Hook 配置存在**：检查 `.codebuddy/settings.json` / `.claude/settings.json` / `.codex/config.toml` 中的 hooks 配置
4. **查看 Hook 日志**：CodeBuddy 插件设置中有 Hooks 选项卡，可查看执行日志和错误信息

### Hook 执行报错

- `python: command not found`：Python 未加入系统 PATH，参考[前置条件](#前置条件)
- `ModuleNotFoundError`：确保 `llm_wiki_hook_utils.py` 与其他 hook 脚本在同一目录
- JSON 解析错误：Hook 脚本通过 stdin 接收输入、stdout 输出 JSON，确保没有额外的 print 语句干扰输出

## 与 RAG 的区别

| 方案 | 知识存在于 | 综合发生在 | 适合 |
|---|---|---|---|
| RAG | 原始 chunk / embedding | 查询时 | 大规模检索 |
| LLM Wiki | 可维护 Markdown 页面 | 摄入和维护时 | 长期复利知识沉淀 |

## License

MIT
