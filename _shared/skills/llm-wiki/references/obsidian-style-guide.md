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

### 标签分类体系

建议按以下维度组织标签，避免随意造词：

| 维度 | 格式 | 示例 |
|------|------|------|
| 工具/平台 | `tool/<name>` | `tool/codebuddy`、`tool/claudecode`、`tool/codex` |
| 主题/领域 | `topic/<name>` | `topic/配置格式`、`topic/安全模型`、`topic/插件系统` |
| 类型 | `type/<name>` | `type/对比`、`type/演进`、`type/实体` |

裸标签（如 `#codebuddy`）也可使用，但嵌套标签优先，便于 Dataview 过滤。

### 各页面类型标签要求

| 页面类型 | tags 要求 | 常见标签示例 |
|----------|----------|-------------|
| source | 至少 1 个主题标签 | `tool/codebuddy`、`topic/配置格式` |
| entity | 至少 1 个工具/平台标签 | `tool/claudecode` |
| concept | 至少 1 个主题标签 + 1 个类型标签 | `topic/安全模型`、`type/对比` |
| analysis | 至少 1 个主题标签 + 1 个类型标签 | `topic/插件系统`、`type/对比` |
| overview | 至少 1 个主题标签 | `topic/ai-coding` |

## 对话引用

- 对话中引用文件使用项目相对路径：`wiki/concepts/perlin-noise.md`。
- wiki 内部仍使用 Obsidian 双链。
