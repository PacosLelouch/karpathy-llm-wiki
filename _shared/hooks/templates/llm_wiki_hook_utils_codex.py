"""
Hook 工具模块 —— Codex 版本。

提供：
- 输出格式适配（format_deny/allow/ask/additional_context）
- 平台特定工具名集合（EDIT_TOOLS）

Hook 脚本通过 from llm_wiki_hook_utils import ... 调用这些函数。

Codex Hook 输出格式规范：
- PreToolUse deny: {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}
- PreToolUse allow + 上下文: {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "..."}}
- PostToolUse 上下文: {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "..."}}

Codex 工具名规范：
- 文件修改：Edit, Write, apply_patch（Edit|Write 可匹配 apply_patch）
- 工具输入：apply_patch 的内容在 tool_input
"""

import json
import sys


# Codex 工具名（官方规范，区分大小写）
EDIT_TOOLS = {'Edit', 'Write', 'apply_patch'}


def format_deny(reason, event_name="PreToolUse"):
    """格式化拒绝决策输出。"""
    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def format_allow(reason=""):
    """格式化允许决策输出（默认不输出任何内容即可放行）。"""
    # Codex: 退出码 0 且无输出 = 成功放行
    # 但为了与其他平台统一，仍输出一个空 JSON
    return {}


def format_ask(reason, event_name="PreToolUse"):
    """格式化询问决策输出。

    Codex 不支持 ask 决策，降级为 deny 并标注需用户确认。
    """
    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "permissionDecision": "deny",
            "permissionDecisionReason": f"[需用户确认] {reason}",
        }
    }


def format_additional_context(message, event_name="PostToolUse"):
    """格式化附加上下文输出（不阻止操作，仅注入提醒）。"""
    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": message,
        }
    }


def output(result):
    """输出 Hook 结果到 stdout 并退出。"""
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)
