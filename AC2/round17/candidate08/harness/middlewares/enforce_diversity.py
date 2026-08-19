"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iterations = hook_input.get("iteration", 0)
    recent_families = hook_input.get("recent_families", [])
    if len(recent_families) < 3 and iterations >= 5:
        return "You've been refining the same family type. Generate proposals from DIFFERENT families (Gaussian, B-spline, oscillatory, multi-level steps, asymmetric exponential)."
    if iterations % 10 == 0 and iterations > 0:
        return "Iteration milestone. Have you explored multiple function families? Call analyze_convolution to guide mutations."
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
