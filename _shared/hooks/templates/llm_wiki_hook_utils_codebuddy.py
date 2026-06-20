"""
Hook 工具模块 —— CodeBuddy 版本。

提供：
- 输出格式适配（format_deny/allow/ask/additional_context）
- 平台特定工具名集合（EDIT_TOOLS）

Hook 脚本通过 from llm_wiki_hook_utils import ... 调用这些函数。
"""

import json
import sys


# 本平台被 hook 拦截的文件修改工具名
EDIT_TOOLS = {'write_to_file', 'replace_in_file'}


def format_deny(reason, event_name="PreToolUse"):
    """格式化拒绝决策输出。"""
    return {"permissionDecision": "deny", "reason": reason}


def format_allow(reason=""):
    """格式化允许决策输出。"""
    result = {"permissionDecision": "allow"}
    if reason:
        result["reason"] = reason
    return result


def format_ask(reason, event_name="PreToolUse"):
    """格式化询问决策输出。"""
    return {"permissionDecision": "ask", "reason": reason}


def format_additional_context(message, event_name="PostToolUse"):
    """格式化附加上下文输出（不阻止操作，仅注入提醒）。"""
    return {"additionalContext": message}


def output(result):
    """输出 Hook 结果到 stdout 并退出。"""
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)
