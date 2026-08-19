"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    return "Ensure you output exactly 4 vertices for square polygons. Check: vertices count = 4, all coords in [0,100000], no self-intersection (axis-aligned squares satisfy this)."
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
