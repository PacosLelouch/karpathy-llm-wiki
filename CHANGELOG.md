# Changelog

本项目遵循面向人类可读的变更日志格式，并尽量按语义化版本管理。

## [Unreleased]

### Fixed
- 修复 ClaudeCode Hook 路径占位符语法：`$CLAUDE_PROJECT_DIR` → `${CLAUDE_PROJECT_DIR}`
- 修复 Codex Hook 配置：添加 `commandWindows` 字段支持 Windows，非 Git 项目回退到 `pwd`

### Added
- 三层架构重构：Skill + Hook + Subagent。
- `_shared/` 真源目录：所有内容在 `_shared/` 维护，通过 sync 脚本生成三平台文件。
- `llm-wiki-raw-guard` Hook：阻止对 `raw/` 已有文件的修改（允许新建）。
- `llm-wiki-post-write-indexer` Hook：wiki/ 写入后提醒更新 index.md 和 log.md。
- `wiki-linter` Subagent：语义性巡检分析，输出结构化巡检报告。
- `ingest-compiler` Subagent：处理复杂摄入编译逻辑。
- `scripts/sync-platforms.py`：从 `_shared/` 真源一键生成 CodeBuddy/Codex/ClaudeCode 三平台文件夹包和插件包。
- 五个操作协议拆分为独立 references 文件（initialize.md、ingest.md、query.md、archive.md、lint.md），按需加载节省 token。
- 三平台 Hook 输出格式适配器（codebuddy_utils.py、codex_utils.py、claude_utils.py）。

### Changed
- SKILL.md 从 ~276 行瘦身为 ~100 行路由文档，详细协议移入 references/。
- validate_repo.py 适配 `_shared/` 新结构，校验真源完整性。
- CONTRIBUTING.md 更新为基于 `_shared/` 真源的开发流程。
- README.md 更新为三层架构 + 多平台生成说明。
- .gitignore 添加 CodeBuddy/、Codex/、ClaudeCode/ 生成目录。
- package_skill.ps1 增加 sync 步骤。

### Removed
- 根目录 `SKILL.md`（移入 `_shared/skills/llm-wiki/SKILL.md`）。
- 根目录 `references/`（移入 `_shared/skills/llm-wiki/references/`）。

## [0.1.0] - 2026-05-18

### Added
- 将 `llm-wiki` 整理为可独立维护的 CodeBuddy skill 仓库。
- 增加五大操作协议：`Initialize`、`Ingest`、`Query`、`Archive`、`Lint`。
- 增加 Obsidian 友好的 `references/` 模板、`examples/` 示例、Bases 与 Canvas 可选视图。
- 增加仓库维护文件、校验脚本和 GitHub 工作流。
- Query 默认只读；只有显式 Ingest、Archive、Lint 自动修复或 Schema/Repo 任务才写文件。
- Lint 分为确定性自动修复和语义性只报告。

### Added
- 初始仓库化版本。
