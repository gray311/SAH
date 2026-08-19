"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    if "constraint" in str(hook_input).lower() or "valid" in str(hook_input).lower():
        return None
    return (
        "CRITICAL: This task requires h(x) ∈ [0,1] and ∫h=1.0. "
        "PRESERVE: sigmoid(latent) activation, penalty_strength parameter, "
        "and integral constraint loss term. Small hyperparameter edits only."
    )
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
