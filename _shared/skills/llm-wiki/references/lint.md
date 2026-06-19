# Lint 操作协议

Lint 分为"确定性自动修复"和"语义性只报告"。

## 可自动修复

仅修复可验证、低风险的问题：

- `wiki/index.md` 漏掉实际存在的 wiki 页面：补条目，摘要可用 `(no summary)` 占位。
- `wiki/index.md` 指向不存在页面：标记 `[MISSING]`，不要直接删除条目。
- wiki 内部链接目标不存在，但能唯一定位到同名文件：修正链接。
- frontmatter 缺少稳定字段：在不改变正文含义的前提下补字段。
- `status`、`type`、`updated` 等字段格式明显不一致：规范化。
- `log.md` 缺少本次 lint 记录：追加记录。

## 只报告，不自动修复

以下依赖语义判断，默认只报告：

- 事实矛盾、来源冲突、过期观点。
- 页面是否应合并、拆分、重命名或废弃。
- 概念定义是否准确。
- 重要概念/实体是否缺页。
- 孤立页面是否真的无价值。
- `mode: archive` 页面引用的来源后来发生重大变化。
- 证据等级是否需要人工调整。

## Post-Lint

追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] lint | 范围
- Issues found: ...
- Auto-fixed: ...
- Report-only: ...
- Remaining: ...
```

详细清单见 `references/lint-checklist.md`。

## 使用 Subagent

语义性巡检建议调用 `wiki-linter` subagent，它能：
- 系统性遍历所有 wiki 页面
- 交叉验证跨页面一致性
- 输出结构化巡检报告（已修复 / 需确认 / 建议）

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
