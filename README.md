# llm-wiki

一个面向 CodeBuddy 的中文 LLM Wiki skill，用于创建、维护、查询、归档和巡检由 LLM 增量维护的 Obsidian/Markdown 知识库。

它吸收 Karpathy LLM Wiki 的核心思想：让 LLM 编写和维护 wiki，人类负责选择资料、提出问题和判断方向。与一次性 RAG 不同，LLM Wiki 会在资料摄入和维护阶段持续编译知识，让知识页面、索引、日志和交叉引用随时间复利增长。

## 适合什么场景

- 个人/团队知识库
- 论文、文章、会议纪要、代码仓库 README、网页剪藏摄入
- Obsidian 双链、frontmatter、Bases、Canvas 管理
- 基于 wiki 的问答、比较、总结和分析
- 问答结果显式归档
- `index.md`、`log.md`、断链、孤立页、冲突、过期内容巡检
- 为项目生成 `AGENTS.md` / `CLAUDE.md` wiki schema

## 核心目录

```text
raw/                         # 原始资料，不修改
  sources/                   # 文章、论文、网页剪藏、转录稿
  assets/                    # 图片、PDF、截图、附件
wiki/                        # LLM 维护的知识层
  index.md                   # 内容索引
  log.md                     # 操作日志
  overview.md                # 全局概览
  sources/                   # 来源摘要页
  entities/                  # 实体页
  concepts/                  # 概念页
  analyses/                  # 分析页和归档页
  timelines/                 # 时间线
  questions.md               # 待研究问题
```

## 五个核心操作

| 操作 | 触发 | 写入行为 |
|---|---|---|
| Initialize | 初始化 wiki 或首次摄入缺结构 | 只创建缺失结构，不覆盖已有文件 |
| Ingest | 摄入 URL/文件/文本/raw 来源 | 更新 raw/wiki/index/log |
| Query | 基于当前 wiki 提问 | 默认只读，不写文件 |
| Archive | 明确要求保存/沉淀/归档 | 新建归档页，更新 index/log |
| Lint | 巡检/修复/补链/健康检查 | 确定性问题可自动修复，语义问题只报告 |

## 快速开始

### 初始化

```text
请使用 llm-wiki skill，初始化当前项目的 wiki 结构，并生成 AGENTS.md。
```

### 摄入资料

```text
请使用 llm-wiki skill，摄入 raw/sources/example.md，并更新相关概念页、实体页、index.md 和 log.md。
```

### 只读查询

```text
请使用 llm-wiki skill，基于当前 wiki 回答：这个主题目前有哪些核心结论？这次只读，不要修改文件。
```

### 显式归档

```text
请使用 llm-wiki skill，把刚才的回答归档为 wiki/analyses 下的 archive 页面，并更新 index.md 和 log.md。
```

### 巡检

```text
请使用 llm-wiki skill，对当前 wiki 做 lint。确定性问题自动修复，语义性问题只报告。
```

## Obsidian 支持

- 使用 `[[concepts/perlin-noise]]` 形式的双链。
- 使用 YAML frontmatter 支持 Properties、Bases、Dataview 和巡检。
- 使用 callout 标注来源、冲突、待验证问题和当前建议。
- 可选 `references/bases-template.base` 作为 wiki 数据库视图。
- 可选 `references/knowledge-map-template.canvas` 展示 raw、wiki、schema 三层关系。

## 模板、示例与仓库维护

- `references/`：raw、source、entity、concept、analysis、archive、index、log、lint、Obsidian、CodeBuddy 模板。
- `examples/`：完整示例，展示 raw 到 source/concept/entity/analysis/archive/index/log 的写法。
- `docs/`：仓库维护、发布清单、设计取舍和使用配方。
- `scripts/`：自包含校验和打包辅助脚本。
- `.github/`：CI、Issue 模板和 PR 模板。

## 仓库结构

```text
llm-wiki/
  SKILL.md                         # CodeBuddy skill 入口
  README.md                        # 使用说明
  references/                      # 详细模板、规范和清单
  examples/                        # 虚构示例
  docs/                            # 仓库维护文档
  scripts/                         # 校验和打包辅助脚本
  assets/                          # 预留资源目录，当前仅含说明文件

  .github/                         # CI、Issue、PR 模板
  CHANGELOG.md
  CONTRIBUTING.md
  SECURITY.md
  CODE_OF_CONDUCT.md
```

## 安装/复制

### 项目级 skill

复制到项目目录：

```text
.codebuddy/skills/llm-wiki/
```

### 用户级 skill

复制到用户级 CodeBuddy skill 目录：

```text
~/.codebuddy/skills/llm-wiki/
```

## 本地校验

先运行仓库自检：

```bash
python -X utf8 scripts/validate_repo.py .
```

可选：使用 CodeBuddy 内置 `skill-creator` 校验脚本：

```bash
python -X utf8 path/to/skill-creator/scripts/quick_validate.py path/to/llm-wiki
```

若要打包：

```bash
python -X utf8 path/to/skill-creator/scripts/package_skill.py path/to/llm-wiki ./dist
```

Windows 可使用辅助脚本：

```powershell
scripts/package_skill.ps1 -SkillCreatorDir "path\to\skill-creator"
```

## 维护文档

- `docs/repository-guide.md`：目录职责和扩展流程。
- `docs/skill-design.md`：设计目标和关键取舍。
- `docs/usage-recipes.md`：常用 CodeBuddy 指令。
- `docs/release-checklist.md`：发布前检查清单。

## 与 RAG 的区别

| 方案 | 知识存在于 | 综合发生在 | 适合 |
|---|---|---|---|
| RAG | 原始 chunk / embedding | 查询时 | 大规模检索 |
| LLM Wiki | 可维护 Markdown 页面 | 摄入和维护时 | 长期复利知识沉淀 |

## License

MIT

