"""
Hook 输出格式适配器 —— Claude Code 版本。

提供 Claude Code 平台特定的 Hook 输出格式化函数。
Hook 脚本通过 from llm_wiki_hook_utils import ... 调用这些函数。

Claude Code 使用 hookSpecificOutput 包装格式。
"""

import json
import sys


def format_deny(reason):
    """格式化拒绝决策输出。"""
    return {
        "hookSpecificOutput": {
            "permissionDecision": "deny",
            "reason": reason
        }
    }


def format_allow():
    """格式化允许决策输出。"""
    return {
        "hookSpecificOutput": {
            "permissionDecision": "allow"
        }
    }


def format_ask(reason):
    """格式化询问决策输出。"""
    return {
        "hookSpecificOutput": {
            "permissionDecision": "ask",
            "reason": reason
        }
    }


def format_additional_context(message):
    """格式化附加上下文输出（不阻止操作，仅注入提醒）。"""
    return {
        "hookSpecificOutput": {
            "additionalContext": message
        }
    }


def output(result):
    """输出 Hook 结果到 stdout 并退出。"""
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0)
