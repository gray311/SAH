"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    score = hook_input.get("current_score", None)
    if iteration == 0:
        return "IMPORTANT: Call generate_variants(5) first to create diverse step function candidates. Do not start with gradient descent alone."
    elif iteration % 8 == 0 and score is not None:
        return "Cycle reminder: If you've been using the same construction method for 8 iterations, call generate_variants to explore a new approach."
    elif score is not None and score < 0.82:
        return "Stalled? Generate new variants and probe them before refining further."
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
