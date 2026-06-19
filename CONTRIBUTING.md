# Contributing

感谢改进 `llm-wiki` skill。提交变更前，请先确认修改是否保持三层架构和渐进披露原则。

## 开发流程

1. 新建分支。
2. 修改 `_shared/` 下的真源文件（SKILL.md、references/、hooks/、agents/）。
3. 运行 sync 生成三平台文件：

```bash
python scripts/sync-platforms.py --format folders
python scripts/sync-platforms.py --format plugins
```

4. 运行本地校验：

```powershell
python -X utf8 scripts/validate_repo.py .
```

5. 更新 `CHANGELOG.md` 的 `[Unreleased]`。
6. 提交 PR。

## 修改什么、在哪里改

| 想改的内容 | 修改位置 | 说明 |
|-----------|---------|------|
| 操作协议、触发、禁忌 | `_shared/skills/llm-wiki/SKILL.md` | 瘦身路由文档，详细协议在 references/ |
| 各操作详细协议 | `_shared/skills/llm-wiki/references/*.md` | Initialize/Ingest/Query/Archive/Lint |
| 模板和清单 | `_shared/skills/llm-wiki/references/*-template.md` | 各类型页面模板 |
| Hook 检测逻辑 | `_shared/hooks/*.py` | 修改后重新 sync |
| Hook 输出格式 | `_shared/hooks/templates/*_utils.py` | 平台适配器 |
| Agent 指令 | `_shared/agents/instructions/*.md` | Subagent 指令 |
| Agent 元数据 | `_shared/agents/agents.yaml` | Agent 触发词和描述 |
| 仓库文档 | `docs/`、`README.md`、`CONTRIBUTING.md` | 不进入 _shared |
| 示例 | `examples/` | 不进入 _shared |

**重要**：不要直接修改 `CodeBuddy/`、`Codex/`、`ClaudeCode/` 或 `dist/` 目录。这些由 `sync-platforms.py` 从 `_shared/` 生成。

## 内容规范

- `SKILL.md` 只保留路由、触发、禁忌和自动化说明，不堆叠完整协议。
- 各操作详细协议放在 `references/initialize.md` 等文件中。
- 模板放在 `references/`。
- 可学习样例放在 `examples/`。
- 仓库维护说明放在 `docs/`。
- Markdown 文件名使用小写英文和短横线。
- 不把真实用户资料、私密知识库内容或大型二进制文件提交到仓库。

## 变更分类

- **协议变更**：修改操作决策路由或五个操作详细协议。
- **模板变更**：修改 `references/` 中的模板。
- **示例变更**：修改 `examples/`。
- **Hook 变更**：修改 `_shared/hooks/`。
- **Agent 变更**：修改 `_shared/agents/`。
- **仓库维护**：修改 `docs/`、`scripts/`、`.github/`。

协议变更应同步更新 SKILL.md、相关模板和示例，并重新运行 sync。
