"""
写入后索引提醒 Hook。

在 Agent 修改 wiki/ 目录下的文件后：
1. 如果修改的不是 index.md 或 log.md，提醒更新 index.md 和 log.md
2. 如果修改的是 index.md 或 log.md，不做提醒

通过 from llm_wiki_hook_utils import ... 调用平台特定的输出格式。
"""

import json
import os
import sys

# Python 运行时自动将脚本所在目录加入 sys.path
from llm_wiki_hook_utils import format_additional_context, format_allow, output, EDIT_TOOLS


def is_wiki_file(filepath):
    """判断文件是否位于 wiki/ 目录下。"""
    if not filepath:
        return False
    normalized = filepath.replace('\\', '/')
    parts = normalized.split('/')
    return len(parts) > 0 and parts[0] == 'wiki'


def is_index_or_log(filepath):
    """判断文件是否为 index.md 或 log.md。"""
    if not filepath:
        return False
    normalized = filepath.replace('\\', '/')
    basename = os.path.basename(normalized)
    return basename in ('index.md', 'log.md')


def main():
    """主入口：读取 stdin 中的 Hook 输入，执行检查，输出结果。"""
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # 无法解析输入，放行
        output(format_allow())

    # 从 Hook 输入中提取工具调用信息
    tool_name = data.get('tool_name', data.get('tool', ''))
    tool_input = data.get('tool_input', data.get('input', {}))

    # 只处理文件修改类工具（使用平台特定的工具名集合）
    # Codex 工具名区分大小写（Edit/Write/apply_patch），用大小写不敏感匹配做兼容
    if tool_name not in EDIT_TOOLS and tool_name.lower() not in {t.lower() for t in EDIT_TOOLS}:
        output(format_allow())

    filepath = tool_input.get('filePath', tool_input.get('path', tool_input.get('file', '')))

    # 不是 wiki/ 目录下的文件，不做提醒
    if not is_wiki_file(filepath):
        output(format_allow())

    # 修改的是 index.md 或 log.md 本身，不需要额外提醒
    if is_index_or_log(filepath):
        output(format_allow())

    # 修改了 wiki/ 下非 index/log 的文件，提醒更新索引和日志
    output(format_additional_context(
        "LLM Wiki 提醒：已修改 wiki/ 下的文件，请确保同步更新：\n"
        "1. wiki/index.md — 新增或更新对应条目的链接、摘要、状态和更新时间\n"
        "2. wiki/log.md — 追加本次操作记录（ingest/archive/lint 等）"
    ))


if __name__ == '__main__':
    main()
