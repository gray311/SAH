"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iterations = hook_input.get("iteration", 0)
    # Force new family exploration after 8 iterations if no significant progress
    if iterations >= 8 and iterations % 5 == 0:
        return "CRITICAL: You've been refining step functions for too long. The best score (1.03857) barely improved from seed (1.03841). STOP REFINING STEPS. Generate an entirely new function family (Gaussian mixtures, splines, oscillatory) using ANALYZE_CONVOLUTION first to understand what's wrong."
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
