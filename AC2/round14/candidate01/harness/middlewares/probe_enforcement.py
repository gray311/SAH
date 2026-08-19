"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    if "evaluate_solution" in hook_input.get("tool_name", ""):
        current_best = hook_input.get("current_best_score", None)
        current_score = hook_input.get("current_score", None)
        if current_best and current_score:
            return "Have you probed this variant? If probe < current_best, skip full eval. Use your 30 probes wisely!"
        return "Remember: probe ALL variants before full evaluation. You have 30 probes!"
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
