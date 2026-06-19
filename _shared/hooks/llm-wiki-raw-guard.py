"""
Raw 不可变守卫 Hook。

在 Agent 执行文件修改操作前检查：
1. 是否修改了 raw/ 目录下的已有文件（禁止）
2. 是否在 raw/ 下创建新文件（允许）

通过 from llm_wiki_hook_utils import ... 调用平台特定的输出格式。
"""

import json
import os
import sys

# Python 运行时自动将脚本所在目录加入 sys.path
from llm_wiki_hook_utils import format_deny, format_allow, output


def is_raw_file(filepath):
    """判断文件是否位于 raw/ 目录下。"""
    if not filepath:
        return False
    # 标准化路径分隔符
    normalized = filepath.replace('\\', '/')
    parts = normalized.split('/')
    return len(parts) > 0 and parts[0] == 'raw'


def is_new_file(tool_input):
    """判断是否为新建文件操作（而非修改已有文件）。

    write_to_file: 总是覆盖写，但如果没有 old_str 说明是新建
    replace_in_file: 总是修改已有文件
    """
    # replace_in_file 总是修改已有文件
    old_str = tool_input.get('old_str', tool_input.get('old_content', ''))
    if old_str:
        return False
    # write_to_file 如果 filePath 对应文件不存在，则是新建
    # Hook 中无法可靠检查文件是否存在，保守处理：
    # 如果有内容但没有 old_str，假定为新建（允许）
    content = tool_input.get('content', tool_input.get('new_str', ''))
    if content and not old_str:
        return True
    return False


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

    # 只拦截文件修改类工具
    edit_tools = {'write_to_file', 'replace_in_file', 'edit_file', 'write', 'edit'}
    if tool_name.lower() not in edit_tools:
        output(format_allow())

    filepath = tool_input.get('filePath', tool_input.get('path', tool_input.get('file', '')))

    # 不在 raw/ 目录下的文件，放行
    if not is_raw_file(filepath):
        output(format_allow())

    # 在 raw/ 下创建新文件，允许
    if is_new_file(tool_input):
        output(format_allow())

    # 检查环境变量是否显式允许修改 raw/
    allow_raw_edit = os.environ.get('LLM_WIKI_ALLOW_RAW_EDIT', '').strip() in ('1', 'true', 'yes')

    if allow_raw_edit:
        output(format_allow())

    # 修改 raw/ 目录下已有文件，拒绝
    output(format_deny(
        f"禁止修改 raw/ 目录下的已有文件：{filepath}。"
        f"raw/ 是不可变证据层，原始资料不应被修改。"
        f"如需修正错误摄入，请在当前会话设置环境变量后重试："
        f"  PowerShell: $env:LLM_WIKI_ALLOW_RAW_EDIT='1'"
        f"  Bash: export LLM_WIKI_ALLOW_RAW_EDIT=1"
    ))


if __name__ == '__main__':
    main()
