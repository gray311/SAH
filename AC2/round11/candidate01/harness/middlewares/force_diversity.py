"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_tool(hook_input):
    score = hook_input.get("last_score", 0)
    iteration = hook_input.get("iteration", 0)
    if score is not None and score < 1.037 and iteration > 20:
        return "DIVERSITY ALERT: Stuck for >20 iterations. Try a COMPLETLY different function class: (a) smooth exponential/Gaussian, (b) spline with optimized knots, (c) multi-Gaussian mixture. Don't just tweak step heights!"
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
