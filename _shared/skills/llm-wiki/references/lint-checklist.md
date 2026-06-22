# LLM Wiki 巡检清单

## 确定性检查：可自动修复

- [ ] `wiki/index.md` 是否漏掉实际存在的 wiki 页面。
- [ ] `wiki/index.md` 是否指向不存在页面；若是，标记 `[MISSING]`。
- [ ] wiki 内部链接是否断裂；若能唯一定位同名目标，则修正。
- [ ] `raw` 引用是否指向真实文件；若能唯一定位，则修正。
- [ ] frontmatter 是否缺少必要字段：`title`、`type`、`created/updated`、`sources`、`status`。
- [ ] `status`、`type`、`mode`、`evidence_level` 是否使用受控值。
- [ ] `tags` 是否缺失或为空数组（source/entity/concept/analysis/overview 页面必须有标签，见 `obsidian-style-guide.md`）。
- [ ] `overview.md` 是否包含与 concept/analysis 页面重复的具体对比内容（应只做入口页，详见 `wiki-schema-template.md`）。
- [ ] 本次 lint 是否已追加到 `wiki/log.md`。

## 语义检查：只报告

- [ ] 跨页面事实是否矛盾。
- [ ] 新来源是否推翻旧说法但未标记冲突。
- [ ] 是否存在过期结论、过时工具或废弃术语。
- [ ] 是否存在孤立页面；它是否真的需要入链。
- [ ] 是否存在频繁被提及但没有独立页面的概念/实体。
- [ ] 是否存在重复概念页，是否建议合并。
- [ ] `mode: archive` 页面引用的来源是否后来发生重大变化。
- [ ] 证据等级是否需要人工复核。

## 输出格式

```markdown
## 巡检结果

### 已自动修复
- ...

### 需要人工确认
- ...

### 建议后续处理
- ...
```
