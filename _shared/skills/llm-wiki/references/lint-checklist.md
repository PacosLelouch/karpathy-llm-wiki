# Lint 确定性检查清单

以下检查可由主 agent 自动执行和修复。语义性检查（矛盾、过期、概念缺口等）由 `llm-wiki-linter` subagent 负责，见 `agents/instructions/llm-wiki-linter.md`。

## 可自动修复

- [ ] `wiki/index.md` 是否漏掉实际存在的 wiki 页面。
- [ ] `wiki/index.md` 是否指向不存在页面；若是，标记 `[MISSING]`。
- [ ] wiki 内部链接是否断裂；若能唯一定位同名目标，则修正。
- [ ] `raw` 引用是否指向真实文件；若能唯一定位，则修正。
- [ ] frontmatter 是否缺少必要字段：`title`、`type`、`created/updated`、`sources`、`status`。
- [ ] `status`、`type`、`mode`、`evidence_level` 是否使用受控值。
- [ ] `tags` 是否缺失或为空数组（source/entity/concept/analysis/overview 页面必须有标签，见 `obsidian-style-guide.md`）。
- [ ] `overview.md` 是否包含与 concept/analysis 页面重复的具体对比内容（应只做入口页，详见 `wiki-schema-template.md`）。
- [ ] 本次 lint 是否已追加到 `wiki/log.md`。
