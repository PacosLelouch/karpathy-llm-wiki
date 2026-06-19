# Release Checklist

发布前检查：

## 1. 内容检查

- [ ] `_shared/skills/llm-wiki/SKILL.md` frontmatter 包含 `name` 和 `description`。
- [ ] `description` 使用第三人称触发语。
- [ ] `SKILL.md` 没有堆叠过长协议，详细内容在 `references/`。
- [ ] `references/` 中五个操作协议完整且一致。
- [ ] `examples/` 中示例不包含真实私密资料。
- [ ] `README.md`、`CHANGELOG.md` 已更新。

## 2. 本地校验

```powershell
python -X utf8 scripts/validate_repo.py .
```

可选 CodeBuddy 校验：

```powershell
python -X utf8 "path\to\skill-creator\scripts\quick_validate.py" _shared/skills/llm-wiki
```

## 3. 生成平台包

```powershell
# 生成文件夹包
python scripts/sync-platforms.py --format folders

# 生成插件包
python scripts/sync-platforms.py --format plugins
```

## 4. 验证生成结果

- [ ] `CodeBuddy/.codebuddy/` 包含 skills/、hooks/、agents/、settings.json。
- [ ] `Codex/.codex/` 包含 hooks/、agents/、config.toml。
- [ ] `Codex/.agents/` 包含 skills/。
- [ ] `ClaudeCode/.claude/` 包含 skills/、hooks/、agents/、settings.json。
- [ ] 各平台 llm_wiki_hook_utils.py 对应正确平台。

## 5. Git

```powershell
git status --short
git tag v2.0.0
```

## 6. 发布说明

发布说明至少包含：

- 核心变化（三层架构重构、多平台生成）
- 兼容性说明（从单 SKILL.md 迁移到 _shared/ 结构）
- 新增 Hook 和 Subagent
- 已知限制
