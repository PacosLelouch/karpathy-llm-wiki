# Contributing

感谢改进 `llm-wiki` skill。提交变更前，请先确认修改是否保持 CodeBuddy skill 的渐进披露原则：`SKILL.md` 保持精炼，详细模板、示例和说明放入 `references/`、`examples/` 或 `docs/`。

## 开发流程

1. 新建分支。
2. 修改 `SKILL.md`、`references/`、`examples/`、`docs/` 或维护脚本。
3. 运行本地校验：

```powershell
python -X utf8 scripts/validate_repo.py .
```

4. 如本机有 CodeBuddy 内置 `skill-creator` 脚本，再运行：

```powershell
python -X utf8 "path\to\skill-creator\scripts\quick_validate.py" .
```

5. 更新 `CHANGELOG.md` 的 `[Unreleased]`。
6. 提交 PR。

## 内容规范

- `SKILL.md` 只保留核心触发、决策和流程，不堆叠完整模板。
- 详细模板放入 `references/`。
- 可学习样例放入 `examples/`。
- 仓库维护说明放入 `docs/`。
- Markdown 文件名使用小写英文和短横线。
- 不把真实用户资料、私密知识库内容或大型二进制文件提交到仓库。

## 变更分类

- **协议变更**：修改 `Initialize/Ingest/Query/Archive/Lint` 行为。
- **模板变更**：修改 `references/`。
- **示例变更**：修改 `examples/`。
- **仓库维护**：修改 `docs/`、`scripts/`、`.github/`。

协议变更应同步更新 `README.md`、相关模板和示例。
