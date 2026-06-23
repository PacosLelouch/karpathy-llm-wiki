# Ingest 操作协议

Ingest = 获取/确认原始资料 + 编译进 wiki + 联动更新 + 更新索引与日志。

## 分流标准

| 场景 | 判断方式 | 处理 |
|------|---------|------|
| **简单摄入** | 单个来源，仅创建/更新 source 页面 + index/log，不涉及 concept/entity/analysis | 主 agent 直接执行 |
| **复杂摄入** | 需要创建 concept/entity/analysis 页面，或需要 cascade 更新已有页面 | 调用 `ingest-compiler` subagent |
| **模糊意图** | 用户只说"摄入这个"，复杂度未知 | 主 agent 快速扫描 raw 内容结构（标题、大纲、关键词），判断是否涉及多概念/实体。复杂则委托 subagent，简单则直接处理 |

## 简单摄入（主 agent 直接执行）

### 1. 读取既有上下文

1. 先读 `wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 和明显相关页面。
2. 搜索是否已有相同来源、同名概念、同一实体或相近分析页。
3. 不凭聊天记忆补事实；事实回到 `raw/` 或已有 wiki 页面验证。

### 2. 处理 raw 来源

- 如果来源已经在 `raw/`：保持原文件不变，只读取。
- 如果用户提供 URL、粘贴文本或外部文件，并明确要求摄入：保存为 `raw/sources/YYYY-MM-DD-short-slug.md` 或领域子路径下的同名文件。
- 文件名使用小写英文、短横线、最多约 60 个字符；日期未知时可不带发布日期，但采集日期仍写入 metadata。
- raw 文件应忠实保存原意，可以清理导航栏、HTML 噪声、重复空白，但不要改写观点。
- 图片、PDF、截图等附件放入 `raw/assets/`，并在 raw/source 页面记录路径。

raw 模板见 `references/raw-template.md`。

### 3. 编译 source 页面

创建或更新 `wiki/sources/` 来源摘要页，提取核心事实和关键信息。

### 4. Post-Ingest

1. 更新 `wiki/index.md`：新增/更新 source 页面的链接、摘要、类型、topic、状态、更新时间、来源数。
2. 追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] ingest | 来源标题或主题
- Raw source: `raw/sources/...`
- Created: `wiki/sources/...`
- Updated: ...
- Cascade updates: ...
- Conflicts / changes: ...
- Follow-up questions: ...
```

## 复杂摄入（调用 `ingest-compiler` subagent）

subagent 输出 YAML 编译方案，主 agent 遍历执行。subagent 的编译策略和 YAML schema 见 `agents/instructions/llm-wiki-ingest-compiler.md`。

### 主 agent 执行 subagent 的 YAML 方案

收到 YAML 后，按字段遍历执行（字段名由 subagent 输出决定）：

1. **`raw_sources`**：确认 raw 文件已保存（`action: created` 时主 agent 保存 raw 文件）
2. **`create_pages`**：按 `content_outline` 创建 wiki 页面，填入完整 frontmatter
3. **`update_pages`**：按 `changes` 描述更新已有页面
4. **`cascade`**：按 `action` 更新 index.md、overview.md、questions.md 等
5. **`conflicts`**：在相关页面添加冲突说明，不静默覆盖旧结论
6. **`follow_ups`**：追加到 `wiki/questions.md`
7. 最后统一更新 `wiki/index.md` 和追加 `wiki/log.md`

如遇 YAML 格式异常，fallback 到人工确认，不自行猜测执行。
