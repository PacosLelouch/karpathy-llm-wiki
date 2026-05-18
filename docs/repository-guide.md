# Repository Guide

## 目录职责

```text
llm-wiki/
  SKILL.md                 # CodeBuddy skill 入口，保持精炼
  README.md                # 面向使用者的总览和快速开始
  references/              # 任务执行时按需加载的详细模板与规范
  examples/                # 可学习的虚构样例
  docs/                    # 仓库维护、发布和设计说明
  scripts/                 # 本仓库维护脚本
  assets/                  # 预留给可复用资源，不放真实用户资料
  .github/                 # PR、Issue 和 CI 配置
```

## 渐进披露规则

- `description`：负责触发。
- `SKILL.md`：负责核心决策和流程。
- `references/`：负责详细模板、清单和样式规则。
- `examples/`：负责展示最终页面长什么样。
- `docs/`：负责仓库维护者如何开发和发布。

## 新增模板时

1. 放入 `references/`。
2. 在 `references/wiki-schema-template.md` 加入口。
3. 必要时在 `examples/` 增加示例。
4. 在 `README.md` 的模板说明中补充。
5. 运行 `python -X utf8 scripts/validate_repo.py .`。

## 修改操作协议时

1. 修改 `SKILL.md`。
2. 同步更新 `README.md` 的五个核心操作表。
3. 同步检查 `references/log-template.md`、`references/lint-checklist.md` 和相关示例。
4. 在 `CHANGELOG.md` 记录。
