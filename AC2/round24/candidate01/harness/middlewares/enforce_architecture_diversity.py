"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    iteration = hook_input.get("iteration", 0)
    tool = hook_input.get("tool_name", "")
    if iteration >= 5 and "step" in hook_input.get("description", "").lower():
        return "Caution: Still focusing on step functions. Call compare_architectures to try Gaussian/B-spline families."
    if iteration >= 10 and tool == "evaluate_solution":
        return "Consider probing more variants before full eval. Try compare_architectures if not done."
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
