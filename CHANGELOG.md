# Changelog

本项目遵循面向人类可读的变更日志格式，并尽量按语义化版本管理。

## [Unreleased]

### Added
- 将 `llm-wiki` 整理为可独立维护的 CodeBuddy skill 仓库。
- 增加五大操作协议：`Initialize`、`Ingest`、`Query`、`Archive`、`Lint`。
- 增加 Obsidian 友好的 `references/` 模板、`examples/` 示例、Bases 与 Canvas 可选视图。
- 增加仓库维护文件、校验脚本和 GitHub 工作流。

### Changed
- Query 默认只读；只有显式 Ingest、Archive、Lint 自动修复或 Schema/Repo 任务才写文件。
- Lint 分为确定性自动修复和语义性只报告。

## [0.1.0] - 2026-05-18

### Added
- 初始仓库化版本。
