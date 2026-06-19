# Repository Guide

## 目录职责

```text
llm-wiki/
  _shared/                     # 开发期真源（仅维护用，运行时不依赖）
    skills/llm-wiki/           # SKILL.md + references/ + README.md
    hooks/                     # 2 个 Hook 主脚本 + templates/（三平台 utils）
    agents/                    # 2 个 Agent 指令 + agents.yaml
    README.md                  # 各平台详细使用指南
  scripts/
    sync-platforms.py          # 真源 → 三平台生成脚本
    validate_repo.py           # 仓库校验脚本
    package_skill.ps1          # Windows 打包辅助
  examples/                    # 可学习的虚构样例
  docs/                        # 仓库维护、发布和设计说明
  assets/                      # 预留给可复用资源，不放真实用户资料
  CodeBuddy/                   # 由 sync 生成，不手动修改
  Codex/                       # 由 sync 生成，不手动修改
  ClaudeCode/                  # 由 sync 生成，不手动修改
  dist/                        # 由 sync 生成，不手动修改
```

## 渐进披露规则

- `description`：负责触发。
- `SKILL.md`：负责操作决策路由、触发场景、禁忌和自动化说明。
- `references/`：负责各操作详细协议、模板、清单和样式规则。
- `examples/`：负责展示最终页面长什么样。
- `docs/`：负责仓库维护者如何开发和发布。

## 修改操作协议时

1. 修改 `_shared/skills/llm-wiki/SKILL.md`（路由）或 `_shared/skills/llm-wiki/references/*.md`（详细协议）。
2. 运行 `python scripts/sync-platforms.py --format folders` 重新生成三平台文件。
3. 同步更新 `README.md` 的五个核心操作表。
4. 同步检查相关模板和示例。
5. 在 `CHANGELOG.md` 记录。
6. 运行 `python -X utf8 scripts/validate_repo.py .`。

## 修改 Hook 时

1. 修改 `_shared/hooks/*.py`（检测逻辑）或 `_shared/hooks/templates/*_utils.py`（平台适配器）。
2. 运行 `python scripts/sync-platforms.py --format folders` 重新生成。
3. 在 `CHANGELOG.md` 记录。

## 修改 Agent 时

1. 修改 `_shared/agents/instructions/*.md`（指令）或 `_shared/agents/agents.yaml`（元数据）。
2. 运行 `python scripts/sync-platforms.py --format folders` 重新生成。
3. 在 `CHANGELOG.md` 记录。

## 新增模板时

1. 放入 `_shared/skills/llm-wiki/references/`。
2. 在 `_shared/skills/llm-wiki/references/wiki-schema-template.md` 加入口。
3. 必要时在 `examples/` 增加示例。
4. 在 `README.md` 的模板说明中补充。
5. 在 `scripts/validate_repo.py` 的 `REQUIRED_REFERENCES` 中补充。
6. 运行 `python scripts/sync-platforms.py --format folders`。
7. 运行 `python -X utf8 scripts/validate_repo.py .`。

## 关于生成目录

`CodeBuddy/`、`Codex/`、`ClaudeCode/` 和 `dist/` 由 `sync-platforms.py` 从 `_shared/` 自动生成。不要手动修改这些目录，修改会在下次 sync 时被覆盖。这些目录应加入 `.gitignore` 或在 CI 中生成。
