# Raw 资料模板

用于 `raw/sources/` 中的原始资料。raw 是证据层，应尽量忠实保存来源内容。

```markdown
---
title: 来源标题
type: raw
source: URL 或来源描述
original_url: URL 或 null
author: 作者或机构
published: YYYY-MM-DD 或 Unknown
collected: YYYY-MM-DD
topic: []
tags: []
status: active
---

# 来源标题

> [!info] Source Metadata
> - Source: URL 或来源描述
> - Author: 作者或机构
> - Published: YYYY-MM-DD 或 Unknown
> - Collected: YYYY-MM-DD

## 原始内容

在这里保存原始正文。可以清理导航栏、HTML 噪声、重复空白和明显抓取错误，但不要改写观点、结论或事实含义。

## 附件

- `raw/assets/...`
```

## 命名规则

- 优先：`YYYY-MM-DD-short-slug.md`
- 日期未知：`short-slug.md`
- 同名冲突：追加 `-2`、`-3`
- slug 使用小写英文、短横线、约 60 字符以内。
