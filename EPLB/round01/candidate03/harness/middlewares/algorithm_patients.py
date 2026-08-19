"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_score = hook_input.get("current_score", None)
    best_so_far = hook_input.get("best_score_so_far", None)
    evals_left = hook_input.get("evals_left", None)
    iteration = hook_input.get("iteration", 0)
    
    if evals_left is not None and evals_left < 6 and iteration > 5:
        return "BUDGET WARNING: <6 evals left, >5 iterations. Consolidate on current best direction. Do not try entirely new algorithm families. Pick the highest-confidence optimization and commit."
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
