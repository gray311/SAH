"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    last_score = hook_input.get('last_score', 0.0)
    evals_used = hook_input.get('evals_used', 0)

    if last_score <= 1.0350 and evals_used < 25:
        return "STUCK: Score <= 1.0350. You are in the seed's local optimum. FORCE a completely new architecture class (ultra-narrow spike, bi-modal, cascade, plateau, or tri-modal). DELETE the EVOLVE-BLOCK and write entirely new function architecture. Do NOT tweak parameters."

    if evals_used > 20:
        return "BUDGET WARNING: Try one more new architecture class with probe before final eval. Don't waste remaining evals on parameter tweaks."

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
