# Release Checklist

发布前检查：

## 1. 内容检查

- [ ] `SKILL.md` frontmatter 包含 `name` 和 `description`。
- [ ] `description` 使用第三人称触发语。
- [ ] `SKILL.md` 没有堆叠过长模板，详细内容在 `references/`。
- [ ] `references/` 中新增模板已被索引。
- [ ] `examples/` 中示例不包含真实私密资料。
- [ ] `README.md`、`CHANGELOG.md` 已更新。

## 2. 本地校验

```powershell
python -X utf8 scripts/validate_repo.py .
```

可选 CodeBuddy 校验：

```powershell
python -X utf8 "path\to\skill-creator\scripts\quick_validate.py" .
```

## 3. 打包

```powershell
python -X utf8 "path\to\skill-creator\scripts\package_skill.py" . .\dist
```

## 4. Git

```powershell
git status --short
git tag v0.1.0
```

## 5. 发布说明

发布说明至少包含：

- 核心变化
- 兼容性说明
- 新增模板/示例
- 已知限制
