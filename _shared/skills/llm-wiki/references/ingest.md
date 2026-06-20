# Ingest 操作协议

Ingest = 获取/确认原始资料 + 编译进 wiki + 联动更新 + 更新索引与日志。

## 1. 读取既有上下文

1. 先读 `wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 和明显相关页面。
2. 搜索是否已有相同来源、同名概念、同一实体或相近分析页。
3. 不凭聊天记忆补事实；事实回到 `raw/` 或已有 wiki 页面验证。

## 2. 处理 raw 来源

- 如果来源已经在 `raw/`：保持原文件不变，只读取。
- 如果用户提供 URL、粘贴文本或外部文件，并明确要求摄入：保存为 `raw/sources/YYYY-MM-DD-short-slug.md` 或领域子路径下的同名文件。
- 文件名使用小写英文、短横线、最多约 60 个字符；日期未知时可不带发布日期，但采集日期仍写入 metadata。
- raw 文件应忠实保存原意，可以清理导航栏、HTML 噪声、重复空白，但不要改写观点。
- 图片、PDF、截图等附件放入 `raw/assets/`，并在 raw/source 页面记录路径。

raw 模板见 `references/raw-template.md`。

## 3. 编译 wiki 页面

根据内容归属选择一个或多个动作：

- 单个来源事实：创建或更新 `wiki/sources/` 来源摘要页。
- 新实体：创建 `wiki/entities/` 页面。
- 新概念：创建 `wiki/concepts/` 页面。
- 跨页面综合、比较、技术选型：创建或更新 `wiki/analyses/` 维护型分析页。
- 时间演进：更新 `wiki/timelines/`。
- 资料缺口：更新 `wiki/questions.md`。

判断规则：

- 同一核心概念已有页面：合并更新，不创建重复页。
- 新来源修正旧说法：保留旧说法来源，新增"争议、矛盾或版本变化"。
- 同一来源影响多个页面：逐一更新受影响页面。
- 页面 `updated` 日期只在知识内容发生变化时刷新。

## 4. Cascade Updates

主页面更新后，检查涟漪影响：

1. 同目录相关页面是否被新资料影响。
2. `wiki/index.md` 中相邻主题或相关条目是否需要更新摘要、状态或链接。
3. `wiki/overview.md` 是否需要更新全局综合理解。
4. `wiki/questions.md` 是否需要新增、关闭或调整问题。
5. 维护型 `analysis` 是否被新证据影响。
6. `mode: archive` 的页面不自动改写；若其引用内容明显过期，只在巡检中报告或标记。

## 5. Post-Ingest

1. 更新 `wiki/index.md`：新增/更新所有被触达页面的链接、摘要、类型、topic、状态、更新时间、来源数。
2. 追加 `wiki/log.md`：

```markdown
## [YYYY-MM-DD] ingest | 来源标题或主题
- Raw source: `raw/sources/...`
- Created: `wiki/sources/...`
- Updated: `wiki/concepts/...`, `wiki/entities/...`, `wiki/analyses/...`
- Cascade updates: ...
- Conflicts / changes: ...
- Follow-up questions: ...
```

## 复杂摄入（必须使用 Subagent）

满足以下**任一**条件时，必须调用 `ingest-compiler` subagent：
- 原始资料文件数 ≥ 5
- 预计生成 ≥ 3 种不同 page type 的 wiki 页面（如同时涉及 source + concept + entity + analysis）
- 摄入内容跨越 ≥ 2 个系统/领域

### subagent 职责

`ingest-compiler` 负责：
1. 读取所有 raw 文件并提取知识结构
2. 输出**编译方案**：哪些文件编译为 source / entity / concept / analysis
3. 规划 **cascade 影响面**：哪些已有页面需要更新
4. 识别可能的概念重叠和冲突

### 主 agent 职责

收到编译方案后，主 agent 负责执行：
- 创建 raw 副本
- 按方案创建/更新 wiki 页面
- 更新 `index.md`、`log.md`、`overview.md`

### 例外

仅在以下情况主 agent 可直接处理（无需 subagent）：
- 单文件摄入，且仅新增/更新 ≤ 2 个 wiki 页面
- 新增内容不涉及概念/实体/分析的交叉引用
