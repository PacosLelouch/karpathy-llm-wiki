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

## 使用 Subagent（必须）

Lint 操作分为两阶段，**必须先调用 subagent**，主 agent 不得跳过：

### 阶段 1：语义性巡检 → 调用 `llm-wiki-linter` subagent

subagent 负责：
- 系统性遍历所有 wiki 页面
- 交叉验证跨页面一致性（事实矛盾、过期内容、重复概念、孤立页）
- 输出结构化巡检报告，包含三类结果：
  - **已自动修复**：subagent 已完成的确定性修复
  - **需要人工确认**：语义性问题，附具体位置与原因
  - **建议后续处理**：合并/拆分/重命名/补页建议

### 阶段 2：确定性修复 → 主 agent 执行

主 agent 收到巡检报告后，执行以下确定性操作：
- 补全 frontmatter 缺失字段
- 修正断链
- 追加 `wiki/log.md` lint 记录

**禁止**：主 agent 不得自行执行语义性巡检来替代 subagent。如果 subagent 不可用，主 agent 应告知用户并仅执行确定性修复。

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
