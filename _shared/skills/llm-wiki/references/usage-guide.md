# LLM Wiki 使用规范

## 常用触发口令

```text
请使用 llm-wiki skill，初始化当前项目的 wiki。
```

```text
请使用 llm-wiki skill，摄入 raw/sources/example.md，并更新相关概念页、index.md 和 log.md。
```

```text
请使用 llm-wiki skill，基于当前 wiki 回答这个问题；这次只读，不要修改文件。
```

```text
请使用 llm-wiki skill，把刚才的回答归档为 analysis 页面，并更新 index.md 和 log.md。
```

```text
请使用 llm-wiki skill，对当前 wiki 做 lint。确定性问题可自动修复，语义性问题只报告。
```

## 执行前读取

- 修改 wiki 前读取 `wiki/index.md`、`wiki/log.md` 和相关页面。
- 修改 schema 前读取本 skill、`references/` 模板和项目级 `AGENTS.md`。
- 用户说"按规范"时，必须先读取规范文件再执行。

## 写入边界

- Query 默认只读。
- Ingest、Archive、Lint 自动修复、Schema/Repo 可写入。
- 不确定是否应写入时，先说明假设；如果普通问答，则不写文件。

## 校验

- 修改 skill 后运行各平台的 skill 校验工具（CodeBuddy: `skill-creator` 的 quick validation）。
- 修改 wiki 后检查：`index.md`、`log.md`、frontmatter、双链、raw 引用。

## 汇报格式

```markdown
完成：...
修改：...
未修改：...
发现：...
后续建议：...
```
