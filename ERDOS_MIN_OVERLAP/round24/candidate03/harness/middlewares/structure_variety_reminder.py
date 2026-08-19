"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    best_score = hook_input.get('best_score', 0.9999)
    evals_used = hook_input.get('evals_used', 0)
    remaining = 30 - evals_used
    if best_score <= 0.999945 and remaining > 10:
        return 'VARY STEP FUNCTION STRUCTURE: Try different block counts (3,4,5,7 blocks), widths (narrower/wider), or value distributions (more extreme 0/1). Do not just tweak hyperparameters. Call generate_discrete_structures again with different patterns.'
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
