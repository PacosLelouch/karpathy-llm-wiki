# Usage Recipes

## 初始化新 wiki

```text
请使用 llm-wiki skill，初始化当前项目的 raw/wiki 结构，并生成 AGENTS.md。
```

## 摄入网页或论文

```text
请使用 llm-wiki skill，摄入这个 URL。先保存 raw，再更新 source、相关 concept/entity、index.md 和 log.md。
```

## 只读查询

```text
请使用 llm-wiki skill，基于当前 wiki 回答这个问题。这次只读，不要修改文件。
```

## 归档一次问答

```text
请使用 llm-wiki skill，把刚才的回答归档到 wiki/analyses，并更新 index.md 和 log.md。
```

## 巡检知识库

```text
请使用 llm-wiki skill，对当前 wiki 做 lint。确定性问题自动修复，语义性问题只报告。
```

## 复杂摄入

当摄入内容涉及多个概念/实体/分析页时，建议指定使用 llm-wiki-ingest-compiler agent：

```text
请使用 llm-wiki skill，摄入这些资料。这个摄入涉及多个概念和实体，请调用 llm-wiki-ingest-compiler agent 协助规划编译策略。
```

## 深度巡检

语义性巡检建议使用 llm-wiki-linter agent：

```text
请使用 llm-wiki skill，对当前 wiki 做完整巡检。请调用 llm-wiki-linter agent 进行语义性分析。
```

## 优化当前 skill 仓库

```text
请使用 llm-wiki skill 和 skill-creator，检查这个 skill 仓库的结构、模板、示例和校验脚本，并提出改进。
```

## 生成多平台包

```bash
# 生成三平台文件夹包
python scripts/sync-platforms.py --format folders

# 生成插件包
python scripts/sync-platforms.py --format plugins
```
