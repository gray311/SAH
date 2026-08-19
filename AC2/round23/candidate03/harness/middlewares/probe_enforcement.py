"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get("tool_name", "")
    probes_used = hook_input.get("probes_used", 0)
    if tool == "evaluate_solution" and probes_used < 5:
        return "CRITICAL: Call probe_solution on at least 5 variants before full eval! You have 30 probes - use them."
    if probes_used >= 20 and tool == "evaluate_solution":
        return "Warning: High probe usage. Ensure you're evaluating truly promising variants."
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def before_tool(self, hook_input):
        try:
            note = before_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
