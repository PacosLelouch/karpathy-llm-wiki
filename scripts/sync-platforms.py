#!/usr/bin/env python3
"""
sync-platforms.py —— 从 _shared/ 真源生成三平台独立可用的文件。

用法：
    python scripts/sync-platforms.py --format folders    # 生成文件夹包（默认）
    python scripts/sync-platforms.py --format plugins    # 生成插件包
    python scripts/sync-platforms.py --install /path/to/project --platform codebuddy  # 安装到项目（合并配置）

folders 模式：生成 CodeBuddy/、Codex/、ClaudeCode/ 三个目录
plugins 模式：生成 dist/ 下的各平台原生插件格式
install 模式：将 LLM Wiki 部署到用户项目目录，自动与已有配置合并（不覆盖其他系统的 hooks）
"""

import argparse
import json
import os
import re
import shutil
import sys
import zipfile

try:
    import yaml
except ImportError as e:
    print(f"错误：无法导入 yaml 模块")
    print(f"请安装 PyYAML：pip install PyYAML")
    print(f"详细错误：{e}")
    sys.exit(1)

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_DIR = os.path.join(ROOT_DIR, '_shared')

# LLM Wiki hooks 标识前缀（用于合并时识别旧版 hooks）
HOOK_PREFIX = 'LLM Wiki '

# ============================================================
# 集中常量定义（单一真源）
# ============================================================

HOOK_NAMES = [
    'llm-wiki-raw-guard.py',
    'llm-wiki-post-write-indexer.py',
]

# 工具模板文件名映射：平台 → 模板文件名
UTILS_TEMPLATE_NAMES = {
    'codebuddy': 'llm_wiki_hook_utils_codebuddy.py',
    'claude':    'llm_wiki_hook_utils_claude.py',
    'codex':     'llm_wiki_hook_utils_codex.py',
}

# 生成的工具模块文件名（统一，各平台 hook 脚本均 import llm_wiki_hook_utils）
UTILS_OUTPUT_NAME = 'llm_wiki_hook_utils.py'

# 各平台被 hook 拦截的文件修改工具名
# Codex 工具名：Edit, Write, apply_patch（Edit|Write 可匹配 apply_patch）
# Claude Code 工具名：Edit, Write, apply_patch（与 Codex 同源）
PLATFORM_EDIT_MATCHERS = {
    'codebuddy': 'write_to_file|replace_in_file',
    'claude':    'Edit|Write|apply_patch',
    'codex':     'Edit|Write|apply_patch',
}


# ============================================================
# 通用辅助函数
# ============================================================

def ensure_dir(path):
    """确保目录存在。"""
    os.makedirs(path, exist_ok=True)


def clean_dir(path):
    """清空并重建目录。"""
    if os.path.exists(path):
        shutil.rmtree(path)
    ensure_dir(path)


def copy_file(src, dst):
    """复制文件。"""
    ensure_dir(os.path.dirname(dst))
    shutil.copy2(src, dst)


def copy_dir(src, dst):
    """递归复制目录。"""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_skill_dir(shared_skills_dir, target_skills_dir):
    """复制 skill 目录（SKILL.md + references + README）。"""
    copy_dir(shared_skills_dir, target_skills_dir)


# ============================================================
# Agent 相关函数
# ============================================================

def read_agents_yaml():
    """读取 agents.yaml 元数据。"""
    yaml_path = os.path.join(SHARED_DIR, 'agents', 'agents.yaml')
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def read_agent_instruction(agent_name):
    """读取 agent 指令内容。"""
    md_path = os.path.join(SHARED_DIR, 'agents', 'instructions', f'{agent_name}.md')
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''


def generate_codebuddy_agent(agent_name, agents_meta):
    """生成 CodeBuddy 格式的 agent（Markdown + YAML frontmatter）。"""
    instruction = read_agent_instruction(agent_name)
    meta = agents_meta.get('agents', {}).get(agent_name, {})

    # 从 YAML frontmatter 提取已有元数据（如果有）
    existing_meta = {}
    if instruction.startswith('---'):
        end = instruction.find('---', 3)
        if end > 0:
            frontmatter = instruction[3:end].strip()
            existing_meta = yaml.safe_load(frontmatter) or {}
            instruction = instruction[end + 3:].strip()

    # 合并元数据
    merged = {**existing_meta, **meta}
    if 'name' not in merged:
        merged['name'] = agent_name

    # 移除 trigger（CodeBuddy agent 不使用 trigger 字段）
    merged.pop('trigger', None)

    frontmatter_str = yaml.dump(merged, allow_unicode=True, default_flow_style=False).strip()

    return f"---\n{frontmatter_str}\n---\n\n{instruction}\n"


def generate_codex_agent(agent_name, agents_meta):
    """生成 Codex 格式的 agent（TOML）。

    Codex 自动扫描 .codex/agents/*.toml，无需在 config.toml 注册。
    必需字段：name、description、developer_instructions。
    """
    instruction = read_agent_instruction(agent_name)
    meta = agents_meta.get('agents', {}).get(agent_name, {})

    # 从 YAML frontmatter 提取已有元数据
    existing_meta = {}
    if instruction.startswith('---'):
        end = instruction.find('---', 3)
        if end > 0:
            frontmatter = instruction[3:end].strip()
            existing_meta = yaml.safe_load(frontmatter) or {}
            instruction = instruction[end + 3:].strip()

    # 合并元数据
    merged = {**existing_meta, **meta}
    if 'name' not in merged:
        merged['name'] = agent_name

    # 生成 TOML
    lines = ['# 由 sync-platforms.py 自动生成，修改请改 _shared/ 下的真源']

    # 简单字段
    for key in ['name', 'description']:
        if key in merged:
            val = merged[key].replace('"', '\\"')
            lines.append(f'{key} = "{val}"')

    # developer_instructions 字段（多行字符串，Codex subagent 必需）
    lines.append('developer_instructions = """')
    lines.append(instruction)
    lines.append('"""')

    return '\n'.join(lines) + '\n'


def generate_claude_agent(agent_name, agents_meta):
    """生成 Claude Code 格式的 agent（与 CodeBuddy 相同：Markdown + YAML）。"""
    return generate_codebuddy_agent(agent_name, agents_meta)


# ============================================================
# Hook 配置生成函数
# ============================================================

def build_llm_wiki_hooks_codebuddy():
    """构建 CodeBuddy 平台的 LLM Wiki hooks 配置列表。"""
    edit_matcher = PLATFORM_EDIT_MATCHERS['codebuddy']
    return {
        "PreToolUse": [
            {
                "matcher": edit_matcher,
                "command": "python \"$CODEBUDDY_PROJECT_DIR/.codebuddy/hooks/llm-wiki-raw-guard.py\"",
                "description": f"{HOOK_PREFIX}Raw 不可变守卫：阻止修改 raw/ 已有文件"
            }
        ],
        "PostToolUse": [
            {
                "matcher": edit_matcher,
                "command": "python \"$CODEBUDDY_PROJECT_DIR/.codebuddy/hooks/llm-wiki-post-write-indexer.py\"",
                "description": f"{HOOK_PREFIX}写入后索引提醒"
            }
        ]
    }


def build_llm_wiki_hooks_claude():
    """构建 Claude Code 平台的 LLM Wiki hooks 配置列表。"""
    edit_matcher = PLATFORM_EDIT_MATCHERS['claude']
    return {
        "PreToolUse": [
            {
                "matcher": edit_matcher,
                "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/llm-wiki-raw-guard.py\"",
                "description": f"{HOOK_PREFIX}Raw 不可变守卫：阻止修改 raw/ 已有文件"
            }
        ],
        "PostToolUse": [
            {
                "matcher": edit_matcher,
                "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/llm-wiki-post-write-indexer.py\"",
                "description": f"{HOOK_PREFIX}写入后索引提醒"
            }
        ]
    }


def build_llm_wiki_hooks_codex():
    """构建 Codex 平台的 LLM Wiki hooks 配置（JSON 格式 dict）。

    Codex hooks.json 格式要求：
    - 每个事件类型下是 matcher group 列表
    - 每个 matcher group 包含 matcher（正则）和 hooks（handler 列表）
    - handler 必须有 type = "command"，以及 command、timeout、statusMessage
    - 命令推荐使用 git root 绝对路径
    """
    edit_matcher = PLATFORM_EDIT_MATCHERS['codex']
    return {
        "PreToolUse": [
            {
                "matcher": edit_matcher,
                "hooks": [
                    {
                        "type": "command",
                        "command": 'python "$(git rev-parse --show-toplevel)/.codex/hooks/llm-wiki-raw-guard.py"',
                        "timeout": 30,
                        "statusMessage": f"{HOOK_PREFIX}Checking raw immutability"
                    }
                ]
            }
        ],
        "PostToolUse": [
            {
                "matcher": edit_matcher,
                "hooks": [
                    {
                        "type": "command",
                        "command": 'python "$(git rev-parse --show-toplevel)/.codex/hooks/llm-wiki-post-write-indexer.py"',
                        "timeout": 30,
                        "statusMessage": f"{HOOK_PREFIX}Post-write index reminder"
                    }
                ]
            }
        ]
    }


# ============================================================
# 配置生成与合并
# ============================================================

def _merge_json_hooks(settings, llm_wiki_hooks):
    """将 LLM Wiki hooks 合并到已有的 settings dict 中。

    策略：按 description 前缀识别旧版 hooks，先移除再追加。
    保留其他系统已注册的 hooks 不受影响。
    """
    settings.setdefault('hooks', {})
    for event in ['PreToolUse', 'PostToolUse']:
        settings['hooks'].setdefault(event, [])
        # 移除旧版 LLM Wiki hooks
        settings['hooks'][event] = [
            h for h in settings['hooks'][event]
            if not h.get('description', '').startswith(HOOK_PREFIX)
        ]
        # 追加当前版本
        settings['hooks'][event].extend(llm_wiki_hooks.get(event, []))
    return settings


def generate_codebuddy_settings(codebuddy_dir, merge=False):
    """生成 CodeBuddy settings.json。

    Args:
        codebuddy_dir: .codebuddy 目录路径
        merge: 若为 True，读取已有 settings.json 并合并（不覆盖其他系统的 hooks）
    """
    settings_path = os.path.join(codebuddy_dir, 'settings.json')
    llm_wiki_hooks = build_llm_wiki_hooks_codebuddy()

    if merge and os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        settings = _merge_json_hooks(settings, llm_wiki_hooks)
    else:
        settings = {'hooks': llm_wiki_hooks}

    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def generate_claude_settings(claude_dir, merge=False):
    """生成 Claude Code settings.json。

    Args:
        claude_dir: .claude 目录路径
        merge: 若为 True，读取已有 settings.json 并合并（不覆盖其他系统的 hooks）
    """
    settings_path = os.path.join(claude_dir, 'settings.json')
    llm_wiki_hooks = build_llm_wiki_hooks_claude()

    if merge and os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        settings = _merge_json_hooks(settings, llm_wiki_hooks)
    else:
        settings = {'hooks': llm_wiki_hooks}

    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def generate_codex_config(codex_dir, merge=False):
    """生成/清理 Codex config.toml。

    Codex 自动扫描 .codex/agents/*.toml，无需在 config.toml 注册 agent。
    hooks 配置使用独立的 hooks.json 文件。
    config.toml 仅用于全局配置（如 [agents] max_threads/max_depth）。

    此函数的主要作用：
    - 全量模式：生成空的最小 config.toml
    - 合并模式：清理旧版 LLM Wiki 残留（[agents.llm-wiki-*] 注册块、[[hooks.*]] 内联 hooks）

    Args:
        codex_dir: .codex 目录路径
        merge: 若为 True，读取已有 config.toml 并清理 LLM Wiki 残留
    """
    config_path = os.path.join(codex_dir, 'config.toml')

    if merge and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        content = _clean_codex_toml(existing_content)
        # 如果清理后内容为空或只有注释，写入最小文件
        stripped = content.strip()
        if not stripped or all(line.strip().startswith('#') or line.strip() == '' for line in stripped.split('\n')):
            content = '# 由 sync-platforms.py 自动生成，修改请改 _shared/ 下的真源\n'
    else:
        # 全量模式：生成最小 config.toml（仅注释）
        content = '# 由 sync-platforms.py 自动生成，修改请改 _shared/ 下的真源\n'

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)


def _merge_codex_hooks_json(settings, llm_wiki_hooks):
    """将 LLM Wiki hooks 合并到已有的 Codex hooks.json 中。

    Codex hooks.json 格式与 CodeBuddy/Claude 不同：
    每个事件类型下是 matcher group 列表，每个 group 包含 matcher + hooks 列表。
    按 statusMessage 前缀识别旧版 LLM Wiki hooks，先移除再追加。
    """
    settings.setdefault('hooks', {})
    # 收集所有涉及的事件类型（已有的 + LLM Wiki 新增的）
    all_events = set(settings['hooks'].keys()) | set(llm_wiki_hooks.keys())
    for event in all_events:
        settings['hooks'].setdefault(event, [])
        # 移除旧版 LLM Wiki hooks：检查 matcher group 中是否有 LLM Wiki handler
        settings['hooks'][event] = [
            group for group in settings['hooks'][event]
            if not any(
                h.get('statusMessage', '').startswith(HOOK_PREFIX)
                for h in group.get('hooks', [])
            )
        ]
        # 追加当前版本
        settings['hooks'][event].extend(llm_wiki_hooks.get(event, []))
    return settings


def generate_codex_hooks_json(codex_dir, merge=False):
    """生成 Codex hooks.json。

    hooks 配置独立于 config.toml，符合 Codex 官方建议：
    "Prefer one representation per layer"。

    Args:
        codex_dir: .codex 目录路径
        merge: 若为 True，读取已有 hooks.json 并合并（不覆盖其他系统的 hooks）
    """
    hooks_path = os.path.join(codex_dir, 'hooks.json')
    llm_wiki_hooks = build_llm_wiki_hooks_codex()

    if merge and os.path.exists(hooks_path):
        with open(hooks_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        settings = _merge_codex_hooks_json(settings, llm_wiki_hooks)
    else:
        settings = {'hooks': llm_wiki_hooks}

    with open(hooks_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def _read_toml_block(lines, start):
    """读取从 start 开始的 TOML 块，返回 (block_lines, next_index)。

    块从 [[...]] 或 [...] 开始，到下一个 [[...]] 或 [...] 或文件结尾结束。
    """
    block = [lines[start]]
    i = start + 1
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('[[') or (stripped.startswith('[') and not stripped.startswith('[[')):
            break
        block.append(lines[i])
        i += 1
    return block, i


def _clean_codex_toml(existing_content):
    """清理 Codex config.toml 中的 LLM Wiki 残留，保留非 LLM Wiki 内容。

    Codex 自动扫描 .codex/agents/*.toml，无需在 config.toml 注册 agent。
    此函数仅做清理，不追加新内容。

    清理范围：
    1. [agents.llm-wiki-*] 命名子表格（旧版注册格式）
    2. [[agents]] 块中 name 以 "llm-wiki-" 开头的（更旧版格式）
    3. [[hooks.*]] 内联 hooks 块（迁移到 hooks.json 后的残留）
    4. 孤立的 [[hooks.*]] matcher 头（hooks 子块已被移除）
    5. LLM Wiki 相关注释行
    """
    lines = existing_content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # === 处理 [agents.llm-wiki-*] 命名子表格（旧版注册格式） ===
        if stripped.startswith('[agents.llm-wiki-') and not stripped.startswith('[['):
            block, i = _read_toml_block(lines, i)
            _remove_preceding_blank_and_comment(result)
            continue

        # === 处理 [[agents]] 块中 name 以 "llm-wiki-" 开头的（更旧版格式） ===
        if stripped == '[[agents]]':
            block, i = _read_toml_block(lines, i)
            is_llm_wiki = any('name = "llm-wiki-' in line or "name = 'llm-wiki-" in line for line in block)
            if is_llm_wiki:
                _remove_preceding_blank_and_comment(result)
                continue
            result.extend(block)
            continue

        # === 处理 [[hooks.*]] 内联 hooks 块（迁移残留清理） ===
        if stripped.startswith('[[hooks.'):
            block, i = _read_toml_block(lines, i)
            is_llm_wiki = any('llm-wiki-' in line or 'LLM Wiki' in line for line in block)
            if is_llm_wiki:
                _remove_preceding_blank_and_comment(result)
                continue
            result.extend(block)
            continue

        # === 跳过 LLM Wiki 相关注释 ===
        if stripped in ('# Hook 配置', '# Agent 定义',
                        '# LLM Wiki Hook 配置', '# LLM Wiki Agent 定义'):
            i += 1
            continue

        # === 其他行直接保留 ===
        result.append(lines[i])
        i += 1

    # 后处理：移除残留的 LLM Wiki 相关注释行
    _comment_set = {
        '# Hook 配置', '# Agent 定义', '# LLM Wiki Hook 配置', '# LLM Wiki Agent 定义',
    }
    result = [line for line in result if line.strip() not in _comment_set]

    # 后处理：清理孤立的 [[hooks.*]] matcher 头
    result = _remove_orphan_hook_matchers(result)

    # 清理连续空行
    result = _collapse_blank_lines(result)

    return '\n'.join(result) + '\n'


def _remove_preceding_blank_and_comment(lines):
    """移除列表末尾连续的空行和 LLM Wiki 相关注释行。"""
    while lines:
        stripped = lines[-1].strip()
        if stripped == '':
            lines.pop()
        elif stripped in ('# Hook 配置', '# Agent 定义',
                          '# LLM Wiki Hook 配置', '# LLM Wiki Agent 定义'):
            lines.pop()
        else:
            break


def _remove_orphan_hook_matchers(lines):
    """移除孤立的 [[hooks.*]] matcher 头。

    当 LLM Wiki 的 [[hooks.*.hooks]] 子块被移除后，其父级 [[hooks.*]] matcher 头
    可能变成孤立项（没有后续的 .hooks 块）。此函数清理这些孤立的 matcher 头。
    """
    result = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        # 检测 [[hooks.*]] matcher 头（非 .hooks 子块）
        if (stripped.startswith('[[hooks.') and ']]' in stripped
                and '.hooks]]' not in stripped):
            # 读取整个 matcher 块
            matcher_block = [lines[i]]
            j = i + 1
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith('[[') or (s.startswith('[') and not s.startswith('[[')):
                    break
                if s == '' or s.startswith('matcher') or s.startswith('#'):
                    matcher_block.append(lines[j])
                    j += 1
                    continue
                break
            # 检查后续是否紧跟 [[hooks.*.hooks]] 块
            k = j
            while k < len(lines) and lines[k].strip() == '':
                k += 1
            has_hooks_block = (k < len(lines)
                               and lines[k].strip().startswith('[[hooks.')
                               and '.hooks]]' in lines[k].strip())
            if has_hooks_block:
                result.extend(matcher_block)
                i = j
            else:
                i = j
                while result and result[-1].strip() == '':
                    result.pop()
        else:
            result.append(lines[i])
            i += 1
    return result


def _collapse_blank_lines(lines):
    """将连续的空行压缩为最多一个。"""
    result = []
    prev_blank = False
    for line in lines:
        if line.strip() == '':
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False
        result.append(line)
    return result


# ============================================================
# 通用部署辅助函数
# ============================================================

def _deploy_hooks(shared_hooks_dir, target_hooks_dir, platform):
    """将 hook 脚本和平台工具模块部署到目标目录。"""
    ensure_dir(target_hooks_dir)
    for hook in HOOK_NAMES:
        copy_file(os.path.join(shared_hooks_dir, hook), os.path.join(target_hooks_dir, hook))
    # 复制平台特定的工具模块，输出名为统一的 llm_wiki_hook_utils.py
    template_name = UTILS_TEMPLATE_NAMES[platform]
    copy_file(
        os.path.join(shared_hooks_dir, 'templates', template_name),
        os.path.join(target_hooks_dir, UTILS_OUTPUT_NAME),
    )


def _deploy_agents(target_agents_dir, agent_names, agents_meta, platform):
    """部署 agent 文件到目标目录。"""
    ensure_dir(target_agents_dir)
    generator = {
        'codebuddy': generate_codebuddy_agent,
        'claude': generate_claude_agent,
        'codex': generate_codex_agent,
    }[platform]
    ext = '.toml' if platform == 'codex' else '.md'
    for name in agent_names:
        content = generator(name, agents_meta)
        with open(os.path.join(target_agents_dir, f'{name}{ext}'), 'w', encoding='utf-8') as f:
            f.write(content)


# ============================================================
# install 模式的清理辅助函数
# ============================================================

# 旧版工具模块文件名（已更名为 llm_wiki_hook_utils.py，需清理残留）
LEGACY_UTILS_FILENAME = 'hook_utils.py'


def _clean_llm_wiki_hooks_dir(target_hooks_dir):
    """清理目标 hooks 目录中的旧版 LLM Wiki 文件。

    清理范围：
    - llm-wiki-*.py（LLM Wiki hook 脚本）
    - llm_wiki_*.py（LLM Wiki 工具模块，如 llm_wiki_hook_utils.py）
    - hook_utils.py（旧版泛化命名的工具模块，升级残留）
    """
    if not os.path.exists(target_hooks_dir):
        return
    for f in os.listdir(target_hooks_dir):
        if f.startswith('llm-wiki-') and f.endswith('.py'):
            os.remove(os.path.join(target_hooks_dir, f))
        elif f.startswith('llm_wiki_') and f.endswith('.py'):
            os.remove(os.path.join(target_hooks_dir, f))
        elif f == LEGACY_UTILS_FILENAME:
            os.remove(os.path.join(target_hooks_dir, f))


def _clean_llm_wiki_agents_dir(target_agents_dir):
    """清理目标 agents 目录中的旧版 LLM Wiki agent 文件。

    清理范围：
    - llm-wiki-*.md / llm-wiki-*.toml（LLM Wiki agent 文件）
    """
    if not os.path.exists(target_agents_dir):
        return
    for f in os.listdir(target_agents_dir):
        if f.startswith('llm-wiki-') and (f.endswith('.md') or f.endswith('.toml')):
            os.remove(os.path.join(target_agents_dir, f))


def _clean_llm_wiki_skills_dir(target_skills_parent_dir):
    """清理目标 skills 父目录中的旧版 LLM Wiki skill 目录。

    清理范围：
    - llm-wiki/ 目录（LLM Wiki skill 目录）
    """
    skill_dir = os.path.join(target_skills_parent_dir, 'llm-wiki')
    if os.path.exists(skill_dir):
        shutil.rmtree(skill_dir)


# ============================================================
# folders 模式
# ============================================================

def generate_folders(output_dir):
    """生成文件夹包模式：CodeBuddy/、Codex/、ClaudeCode/。"""
    shared_skills = os.path.join(SHARED_DIR, 'skills', 'llm-wiki')
    shared_hooks = os.path.join(SHARED_DIR, 'hooks')
    agents_meta = read_agents_yaml()
    agent_names = list(agents_meta.get('agents', {}).keys())

    # 确保至少有默认的 agent 列表
    if not agent_names:
        instructions_dir = os.path.join(SHARED_DIR, 'agents', 'instructions')
        if os.path.exists(instructions_dir):
            agent_names = [
                os.path.splitext(f)[0]
                for f in os.listdir(instructions_dir)
                if f.endswith('.md')
            ]

    # ========== CodeBuddy ==========
    codebuddy_dir = os.path.join(output_dir, 'CodeBuddy', '.codebuddy')

    _deploy_hooks(shared_hooks, os.path.join(codebuddy_dir, 'hooks'), 'codebuddy')
    _deploy_agents(os.path.join(codebuddy_dir, 'agents'), agent_names, agents_meta, 'codebuddy')
    copy_skill_dir(shared_skills, os.path.join(codebuddy_dir, 'skills', 'llm-wiki'))
    generate_codebuddy_settings(codebuddy_dir)

    # ========== Codex ==========
    codex_dir = os.path.join(output_dir, 'Codex', '.codex')
    agents_dir = os.path.join(output_dir, 'Codex', '.agents')

    _deploy_hooks(shared_hooks, os.path.join(codex_dir, 'hooks'), 'codex')
    _deploy_agents(os.path.join(codex_dir, 'agents'), agent_names, agents_meta, 'codex')
    copy_skill_dir(shared_skills, os.path.join(agents_dir, 'skills', 'llm-wiki'))
    generate_codex_config(codex_dir)
    generate_codex_hooks_json(codex_dir)

    # ========== ClaudeCode ==========
    claude_dir = os.path.join(output_dir, 'ClaudeCode', '.claude')

    _deploy_hooks(shared_hooks, os.path.join(claude_dir, 'hooks'), 'claude')
    _deploy_agents(os.path.join(claude_dir, 'agents'), agent_names, agents_meta, 'claude')
    copy_skill_dir(shared_skills, os.path.join(claude_dir, 'skills', 'llm-wiki'))
    generate_claude_settings(claude_dir)


# ============================================================
# plugins 模式
# ============================================================

def generate_plugins(output_dir):
    """生成插件包模式。"""
    dist_dir = os.path.join(output_dir, 'dist')
    clean_dir(dist_dir)

    shared_skills = os.path.join(SHARED_DIR, 'skills', 'llm-wiki')
    shared_hooks = os.path.join(SHARED_DIR, 'hooks')
    agents_meta = read_agents_yaml()
    agent_names = list(agents_meta.get('agents', {}).keys())

    if not agent_names:
        instructions_dir = os.path.join(SHARED_DIR, 'agents', 'instructions')
        if os.path.exists(instructions_dir):
            agent_names = [
                os.path.splitext(f)[0]
                for f in os.listdir(instructions_dir)
                if f.endswith('.md')
            ]

    # ========== Claude Code 插件（一体化） ==========
    claude_plugin_dir = os.path.join(dist_dir, 'claude-llm-wiki-plugin')

    # .claude-plugin/plugin.json
    ensure_dir(os.path.join(claude_plugin_dir, '.claude-plugin'))
    plugin_json = {
        "name": "llm-wiki",
        "description": "LLM Wiki 知识库系统——Skill + Hook + Subagent 三层架构",
        "version": "2.0.0"
    }
    with open(os.path.join(claude_plugin_dir, '.claude-plugin', 'plugin.json'), 'w', encoding='utf-8') as f:
        json.dump(plugin_json, f, ensure_ascii=False, indent=2)

    # skills
    copy_skill_dir(shared_skills, os.path.join(claude_plugin_dir, 'skills', 'llm-wiki'))

    # hooks
    _deploy_hooks(shared_hooks, os.path.join(claude_plugin_dir, 'hooks'), 'claude')

    # agents
    _deploy_agents(os.path.join(claude_plugin_dir, 'agents'), agent_names, agents_meta, 'claude')

    # marketplace.json
    marketplace = {
        "name": "llm-wiki",
        "owner": "llm-wiki",
        "plugins": [
            {
                "name": "llm-wiki",
                "description": "LLM Wiki 知识库系统",
                "version": "2.0.0"
            }
        ]
    }
    with open(os.path.join(claude_plugin_dir, 'marketplace.json'), 'w', encoding='utf-8') as f:
        json.dump(marketplace, f, ensure_ascii=False, indent=2)

    # ========== CodeBuddy 插件（Skills ZIP + 辅助配置） ==========
    codebuddy_plugin_dir = os.path.join(dist_dir, 'codebuddy-llm-wiki-plugin')
    ensure_dir(codebuddy_plugin_dir)

    # Skills ZIP
    skill_zip_path = os.path.join(codebuddy_plugin_dir, 'llm-wiki.zip')
    with zipfile.ZipFile(skill_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(shared_skills):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, shared_skills)
                zf.write(file_path, arcname)

    # settings-hooks.json（用户需合并到 .codebuddy/settings.json）
    generate_codebuddy_settings(codebuddy_plugin_dir)
    # 重命名为 settings-hooks.json
    os.rename(
        os.path.join(codebuddy_plugin_dir, 'settings.json'),
        os.path.join(codebuddy_plugin_dir, 'settings-hooks.json'),
    )

    # agents
    _deploy_agents(os.path.join(codebuddy_plugin_dir, 'agents'), agent_names, agents_meta, 'codebuddy')

    # ========== Codex 插件（文件夹包，无原生插件格式） ==========
    codex_plugin_dir = os.path.join(dist_dir, 'codex-llm-wiki-plugin')

    # .codex/
    codex_dot_codex = os.path.join(codex_plugin_dir, '.codex')
    ensure_dir(codex_dot_codex)

    # hooks
    _deploy_hooks(shared_hooks, os.path.join(codex_dot_codex, 'hooks'), 'codex')

    # agents
    _deploy_agents(os.path.join(codex_dot_codex, 'agents'), agent_names, agents_meta, 'codex')

    # config.toml（最小化，仅注释）
    generate_codex_config(codex_dot_codex)

    # hooks.json
    generate_codex_hooks_json(codex_dot_codex)

    # .agents/skills
    copy_skill_dir(shared_skills, os.path.join(codex_plugin_dir, '.agents', 'skills', 'llm-wiki'))


# ============================================================
# install 模式（合并而非覆写）
# ============================================================

def install_to_project(project_dir, platform):
    """将 LLM Wiki 部署到用户项目目录，自动与已有配置合并。

    与 folders/plugins 模式的区别：
    - 配置文件（settings.json/config.toml/hooks.json）采用合并策略，保留其他系统的 hooks
    - agents/skills 文件直接覆盖（LLM Wiki 专属，不会冲突）
    """
    shared_skills = os.path.join(SHARED_DIR, 'skills', 'llm-wiki')
    shared_hooks = os.path.join(SHARED_DIR, 'hooks')
    agents_meta = read_agents_yaml()
    agent_names = list(agents_meta.get('agents', {}).keys())

    if not agent_names:
        instructions_dir = os.path.join(SHARED_DIR, 'agents', 'instructions')
        if os.path.exists(instructions_dir):
            agent_names = [
                os.path.splitext(f)[0]
                for f in os.listdir(instructions_dir)
                if f.endswith('.md')
            ]

    platforms = [platform] if platform != 'all' else ['codebuddy', 'claude', 'codex']

    for plat in platforms:
        if plat == 'codebuddy':
            plat_dir = os.path.join(project_dir, '.codebuddy')
            _install_codebuddy(plat_dir, shared_hooks, shared_skills, agent_names, agents_meta)
        elif plat == 'claude':
            plat_dir = os.path.join(project_dir, '.claude')
            _install_claude(plat_dir, shared_hooks, shared_skills, agent_names, agents_meta)
        elif plat == 'codex':
            codex_dir = os.path.join(project_dir, '.codex')
            agents_dir = os.path.join(project_dir, '.agents')
            _install_codex(codex_dir, agents_dir, shared_hooks, shared_skills, agent_names, agents_meta)
        else:
            print(f'未知平台：{plat}，跳过')

    print(f'LLM Wiki 已安装到 {project_dir}（平台：{", ".join(platforms)}）')
    print('配置文件已合并，其他系统的 hooks 不受影响。')


def _install_codebuddy(plat_dir, shared_hooks, shared_skills, agent_names, agents_meta):
    """安装 CodeBuddy 平台。"""
    ensure_dir(plat_dir)
    # 清理旧版 LLM Wiki 文件（处理升级场景）
    _clean_llm_wiki_hooks_dir(os.path.join(plat_dir, 'hooks'))
    _clean_llm_wiki_agents_dir(os.path.join(plat_dir, 'agents'))
    _clean_llm_wiki_skills_dir(os.path.join(plat_dir, 'skills'))
    # 部署新版
    _deploy_hooks(shared_hooks, os.path.join(plat_dir, 'hooks'), 'codebuddy')
    _deploy_agents(os.path.join(plat_dir, 'agents'), agent_names, agents_meta, 'codebuddy')
    copy_skill_dir(shared_skills, os.path.join(plat_dir, 'skills', 'llm-wiki'))
    # 合并配置（不覆盖其他系统的 hooks）
    generate_codebuddy_settings(plat_dir, merge=True)


def _install_claude(plat_dir, shared_hooks, shared_skills, agent_names, agents_meta):
    """安装 Claude Code 平台。"""
    ensure_dir(plat_dir)
    # 清理旧版 LLM Wiki 文件
    _clean_llm_wiki_hooks_dir(os.path.join(plat_dir, 'hooks'))
    _clean_llm_wiki_agents_dir(os.path.join(plat_dir, 'agents'))
    _clean_llm_wiki_skills_dir(os.path.join(plat_dir, 'skills'))
    # 部署新版
    _deploy_hooks(shared_hooks, os.path.join(plat_dir, 'hooks'), 'claude')
    _deploy_agents(os.path.join(plat_dir, 'agents'), agent_names, agents_meta, 'claude')
    copy_skill_dir(shared_skills, os.path.join(plat_dir, 'skills', 'llm-wiki'))
    generate_claude_settings(plat_dir, merge=True)


def _install_codex(codex_dir, agents_dir, shared_hooks, shared_skills, agent_names, agents_meta):
    """安装 Codex 平台。"""
    ensure_dir(codex_dir)
    # 清理旧版 LLM Wiki 文件
    _clean_llm_wiki_hooks_dir(os.path.join(codex_dir, 'hooks'))
    _clean_llm_wiki_agents_dir(os.path.join(codex_dir, 'agents'))
    _clean_llm_wiki_skills_dir(os.path.join(agents_dir, 'skills'))
    # 部署新版
    _deploy_hooks(shared_hooks, os.path.join(codex_dir, 'hooks'), 'codex')
    _deploy_agents(os.path.join(codex_dir, 'agents'), agent_names, agents_meta, 'codex')
    copy_skill_dir(shared_skills, os.path.join(agents_dir, 'skills', 'llm-wiki'))
    # 合并配置（清理旧版 config.toml 中的 LLM Wiki 残留，hooks 独立到 hooks.json）
    generate_codex_config(codex_dir, merge=True)
    generate_codex_hooks_json(codex_dir, merge=True)


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='从 _shared/ 真源生成三平台独立可用的文件')
    parser.add_argument(
        '--format',
        choices=['folders', 'plugins'],
        default='folders',
        help='输出格式：folders（文件夹包）或 plugins（插件包）'
    )
    parser.add_argument(
        '--output',
        default=ROOT_DIR,
        help='输出目录（默认为项目根目录）'
    )
    parser.add_argument(
        '--install',
        metavar='PROJECT_DIR',
        help='将 LLM Wiki 安装到指定项目目录（合并配置，不覆盖其他系统 hooks）'
    )
    parser.add_argument(
        '--platform',
        choices=['codebuddy', 'claude', 'codex', 'all'],
        default='all',
        help='安装目标平台（仅 --install 模式，默认 all）'
    )

    args = parser.parse_args()

    if args.install:
        # install 模式
        project_dir = os.path.abspath(args.install)
        if not os.path.isdir(project_dir):
            print(f'错误：项目目录不存在：{project_dir}')
            return
        install_to_project(project_dir, args.platform)
    elif args.format == 'folders':
        # 清理旧输出
        for d in ['CodeBuddy', 'Codex', 'ClaudeCode']:
            clean_dir(os.path.join(args.output, d))
        generate_folders(args.output)
        print('已生成：')
        print(f'  {os.path.join(args.output, "CodeBuddy/")}')
        print(f'  {os.path.join(args.output, "Codex/")}')
        print(f'  {os.path.join(args.output, "ClaudeCode/")}')
    else:
        generate_plugins(args.output)
        print('已生成：')
        print(f'  {os.path.join(args.output, "dist", "claude-llm-wiki-plugin/")}')
        print(f'  {os.path.join(args.output, "dist", "codebuddy-llm-wiki-plugin/")}')
        print(f'  {os.path.join(args.output, "dist", "codex-llm-wiki-plugin/")}')


if __name__ == '__main__':
    main()
