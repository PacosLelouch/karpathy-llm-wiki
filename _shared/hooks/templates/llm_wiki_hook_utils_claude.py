"""
Hook 工具模块 —— Claude Code 版本。

提供：
- 输出格式适配（format_deny/allow/ask/additional_context）
- 平台特定工具名集合（EDIT_TOOLS）

Hook 脚本通过 from llm_wiki_hook_utils import ... 调用这些函数。

Claude Code 使用 hookSpecificOutput 包装格式。
PostToolUse 的 additionalContext 通过 systemMessage 字段注入。
"""

import json
import sys


# Claude Code 工具名（与 Codex 同源，区分大小写）
EDIT_TOOLS = {'Edit', 'Write', 'apply_patch'}


def _wrap(decision, reason="", hook_event="PreToolUse"):
    """Claude Code 的 hook 输出需要 hookSpecificOutput 包装。"""
    result = {
        "hookSpecificOutput": {
            "hookEventName": hook_event,
            "permissionDecision": decision
        }
    }
    if reason:
        result["hookSpecificOutput"]["permissionDecisionReason"] = reason
    return result


def format_deny(reason, event_name="PreToolUse"):
    """格式化拒绝决策输出。"""
    return _wrap("deny", reason, event_name)


def format_allow(reason=""):
    """格式化允许决策输出。"""
    return _wrap("allow", reason)


def format_ask(reason, event_name="PreToolUse"):
    """格式化询问决策输出。"""
    return _wrap("ask", reason, event_name)


def format_additional_context(message, event_name="PostToolUse"):
    """格式化附加上下文输出（不阻止操作，仅注入提醒）。

    Claude Code 通过 systemMessage 字段注入额外上下文。
    """
    return {
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "permissionDecision": "allow"
        }
    }


def output(result):
    """输出 Hook 结果到 stdout 并退出。"""
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)
