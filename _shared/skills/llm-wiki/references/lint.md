# Lint 操作协议

## 分流标准

| 场景 | 判断方式 | 处理 |
|------|---------|------|
| **快速巡检** | 用户明确要求修断链、补 frontmatter、同步索引等确定性检查 | 主 agent 直接执行 |
| **深度巡检** | 用户明确要求检查矛盾、过期、概念缺口、重复页等语义性问题 | 调用 `llm-wiki-linter` subagent |
| **模糊意图** | 用户只说"做个 lint"，未明确范围 | 主 agent 先执行快速巡检，再根据 wiki 规模和发现的问题迹象建议是否需要深度巡检，由用户确认 |

## 快速巡检（主 agent 直接执行）

读取 `references/lint-checklist.md`，逐项检查并修复。该清单是确定性检查的唯一真源，深度巡检的 subagent 也引用同一清单。

## 深度巡检（调用 `llm-wiki-linter` subagent）

subagent 输出 YAML 结构化报告，主 agent 遍历执行。subagent 的分析方法论和 YAML schema 见 `agents/instructions/llm-wiki-linter.md`。

### 主 agent 执行 subagent 的 YAML 报告

收到 YAML 后，按字段遍历执行（字段名由 subagent 输出决定，主 agent 无需预知 schema）：

1. **`auto_fixed`**：subagent 已完成的确定性修复，主 agent 仅记录到 `wiki/log.md`
2. **`needs_review`**：语义性问题，整理为人类可读报告呈现给用户，不自动修复
3. **`suggestions`**：合并/拆分/重命名建议，呈现给用户

如遇 YAML 格式异常（字段缺失、类型不符），fallback 到人工确认，不自行猜测执行。

## Post-Lint

追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] lint | 范围
- Mode: quick | deep
- Issues found: ...
- Auto-fixed: ...
- Report-only: ...
- Remaining: ...
```

如果 subagent 不可用，主 agent 仅执行快速巡检，并告知用户深度巡检未执行。
