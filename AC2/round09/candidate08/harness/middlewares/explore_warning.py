"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_score = hook_input.get("best_score", 0.0)
    if current_score <= 1.0:  # Haven't beaten seed's normalized score
        return "⚠️ SCORE NOT YET ABOVE BASELINE (1.03431). STOP making incremental edits. You need a COMPLETELY new function family: try splines, Fourier optimization, or Gaussian mixtures. The seed's step functions are optimal - beat them with orthogonal mathematical structures."
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
