"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_tool(hook_input):
    iterations = hook_input.get("iteration", 0)
    current_family = hook_input.get("current_family", "")
    family_switch_count = hook_input.get("family_switch_count", 0)
    if current_family and iterations >= 4 and family_switch_count < 5:
        return f"ALERT: You've been working with {current_family} for 3+ iterations. STEP FUNCTION REFINEMENT HAS FAILED. Time to try a completely different family (Gaussian, spline, oscillatory, or piecewise). Do NOT spend more iterations refining this same type. Generate new candidates now."
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def after_tool(self, hook_input):
        try:
            note = after_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
