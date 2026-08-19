"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iterations = hook_input.get("iteration", 0)
    current_best = hook_input.get("best_score", 0)

    if iterations >= 8:
        return "WARNING: You've done many iterations on similar architectures. Have you tried a COMPLETELY DIFFERENT function family? (Gaussian, spline, oscillatory, etc.) Don't keep refining the same type!"
    elif iterations >= 3 and current_best <= 1.03841:
        return "You're not beating the record. Try a NEW function architecture immediately, not another refinement."
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
