# Obsidian 写作规范

## 双链

- wiki 内部语义链接优先使用 `[[路径/文件名]]`：`[[concepts/perlin-noise]]`。
- 显示名使用 `[[concepts/perlin-noise|Perlin Noise]]`。
- 新建页面时补充出链；重要页面应争取有入链。

## Frontmatter

推荐字段：

```yaml
---
title: 页面标题
type: source | entity | concept | analysis | archive | timeline
topic: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
raw: []
tags: []
status: stub | active | mature | outdated | conflicting
evidence_level: primary | secondary | synthesized | speculative
mode: maintained | archive
---
```

## Callouts

```markdown
> [!info] 来源
> 记录来源、采集时间、证据等级。

> [!warning] 冲突
> 记录不同来源之间的差异。

> [!question] 待验证
> 记录资料缺口和后续问题。

> [!tip] 当前建议
> 记录可执行结论。
```

## 附件和嵌入

- 图片、PDF、截图等放入 `raw/assets/`。
- 页面内可用 `![[../raw/assets/file.png]]` 或普通相对链接。
- 不使用本地绝对路径作为长期链接。

## 标签

- frontmatter `tags` 用于结构化检索。
- 正文内标签只用于人类阅读或临时标注。
- 可用嵌套标签：`pcg/noise`、`status/conflicting`。

## 对话引用

- 对话中引用文件使用项目相对路径：`wiki/concepts/perlin-noise.md`。
- wiki 内部仍使用 Obsidian 双链。
