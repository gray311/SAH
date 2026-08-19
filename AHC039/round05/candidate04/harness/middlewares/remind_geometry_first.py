"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    recent_tools = [h.get("tool_name", "") for h in history[-10:]]
    if "analyze_geometry" not in recent_tools:
        return "Strategy reminder: The task requires constructing an orthogonal polygon around mackerel clusters while avoiding sardines. Call analyze_geometry() once early to get mackerel/sardine bounding boxes and overlap estimates. Use these to guide your polygon construction. Don't guess blindly - data analysis first!"
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def before_model(self, hook_input):
        try:
            note = before_model(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
