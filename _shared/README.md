# LLM Wiki ——各平台详细使用指南

本文档详细描述如何使用 LLM Wiki 系统管理知识库，覆盖三个平台：CodeBuddy、Codex、Claude Code。

## 系统架构

LLM Wiki 由三层组成：

| 层 | 功能 | 执行方式 |
|---|---|---|
| **Skill** | 操作性协议、参考文件、模板、清单 | Agent 读取 SKILL.md 后按协议选择参考文件 |
| **Hook** | 硬约束自动执行 | 平台在特定事件时自动调用 |
| **Subagent** | 专项推理分析 | Agent 需要深度分析时调用 |

## 各平台使用方式

### CodeBuddy

1. **安装**：将 `CodeBuddy/.codebuddy/` 目录复制到项目根目录
   ```bash
   cp -r CodeBuddy/.codebuddy /path/to/your/project/
   ```

2. **Skills 生效**：CodeBuddy 自动加载 `.codebuddy/skills/` 下的技能

3. **Hooks 生效**：`.codebuddy/settings.json` 中配置的 Hook 自动执行
   - 修改文件前：`llm-wiki-raw-guard` 阻止对 raw/ 的修改
   - 修改文件后：`llm-wiki-post-write-indexer` 提醒更新 index.md/log.md

4. **Agents 使用**：`.codebuddy/agents/` 下的 agent 定义在对话中可被调用

### Codex

1. **安装**：将 `Codex/` 下的两个目录复制到项目根目录
   ```bash
   cp -r Codex/.codex /path/to/your/project/
   cp -r Codex/.agents /path/to/your/project/
   ```

2. **Skills 生效**：Codex 自动加载 `.agents/skills/` 下的技能

3. **Hooks 生效**：`.codex/config.toml` 中配置的 Hook 自动执行

4. **Agents 使用**：`.codex/agents/` 下的 TOML 格式 agent 定义

### Claude Code

1. **安装**：将 `ClaudeCode/.claude/` 目录复制到项目根目录
   ```bash
   cp -r ClaudeCode/.claude /path/to/your/project/
   ```

2. **Skills 生效**：Claude Code 自动加载 `.claude/skills/` 下的技能

3. **Hooks 生效**：`.claude/settings.json` 中配置的 Hook 自动执行
   - Hook 使用 `$CLAUDE_PROJECT_DIR` 环境变量定位脚本

4. **Agents 使用**：`.claude/agents/` 下的 Markdown+YAML 格式 agent 定义

## 五个核心操作

| 操作 | 触发 | 写入行为 |
|---|---|---|
| Initialize | 初始化 wiki 或首次摄入缺结构 | 只创建缺失结构，不覆盖已有文件 |
| Ingest | 摄入 URL/文件/文本/raw 来源 | 更新 raw/wiki/index/log |
| Query | 基于当前 wiki 提问 | 默认只读，不写文件 |
| Archive | 明确要求保存/沉淀/归档 | 新建归档页，更新 index/log |
| Lint | 巡检/修复/补链/健康检查 | 确定性问题可自动修复，语义问题只报告 |

## Hook 工作原理

Hook 脚本通过 `llm_wiki_hook_utils.py` 适配不同平台的输出格式：

```
llm-wiki-raw-guard.py       →  from llm_wiki_hook_utils import format_deny, format_allow, output
                               → CodeBuddy: {"permissionDecision": "deny", "reason": "..."}
                               → Codex:     {"permissionDecision": "deny", "reason": "..."}
                               → Claude:    {"hookSpecificOutput": {"permissionDecision": "deny", ...}}

llm-wiki-post-write-indexer.py → from llm_wiki_hook_utils import format_additional_context, output
                               → CodeBuddy: {"additionalContext": "..."}
                               → Codex:     {"additionalContext": "..."}
                               → Claude:    {"hookSpecificOutput": {"additionalContext": ...}}
```

每个平台有自己的 `llm_wiki_hook_utils.py`，输出格式硬编码，不做运行时平台检测。

## 参考文件速查

| 用途 | 参考文件 |
|------|---------|
| Initialize 详细协议 | `references/initialize.md` |
| Ingest 详细协议 | `references/ingest.md` |
| Query 详细协议 | `references/query.md` |
| Archive 详细协议 | `references/archive.md` |
| Lint 详细协议 | `references/lint.md` |
| Raw 资料模板 | `references/raw-template.md` |
| 来源页模板 | `references/source-template.md` |
| 概念页模板 | `references/concept-template.md` |
| 实体页模板 | `references/entity-template.md` |
| 分析页模板 | `references/analysis-template.md` |
| 归档页模板 | `references/archive-template.md` |
| Index 模板 | `references/index-template.md` |
| Log 模板 | `references/log-template.md` |
| Schema 总纲模板 | `references/wiki-schema-template.md` |
| Obsidian 写作规范 | `references/obsidian-style-guide.md` |
| 平台通用使用规范 | `references/usage-guide.md` |
| 巡检清单 | `references/lint-checklist.md` |
| Bases 视图模板 | `references/bases-template.base` |
| Canvas 知识地图模板 | `references/knowledge-map-template.canvas` |
