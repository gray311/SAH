"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_score = hook_input.get("current_score")
    if current_score is not None and current_score < 1.0:
        return (
            "Warning: Score below 1.0 (seed=0.999641). The seed's 8000-interval gradient approach may be "
            "fundamentally misaligned for step functions. Consider: (1) Coarse-to-fine (16-512 intervals), "
            "(2) Explicit pattern initialization, (3) Quantized value ranges, (4) Boundary-first optimization. "
            "Don't just tune hyperparameters - change the search paradigm."
        )
    elif current_score is not None:
        return (
            f"Score {current_score:.4f}. If > 1.0, you've made progress! Continue refining. "
            "Remember: step functions need discrete/structured approaches, not just gradient descent."
        )
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
