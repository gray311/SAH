"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    best_score = hook_input.get("best_score", 0)
    evals_left = hook_input.get("evals_left", 20)
    note = None
    if evals_left > 10:
        note = "REMEMBER: Use numpy-based det every 5000 iterations. Keep each search under 150s. Use probe_solution to rank 2-3 variants before evaluate_solution. Only use evaluate_solution ONCE with your best variant."
    return note
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
