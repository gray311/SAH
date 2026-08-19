"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    evals_left = hook_input.get("evaluations_left", 10)
    iteration = hook_input.get("iteration", 1)
    
    if iteration <= 10:
        return "Parametrize your search: try grid sizes 50/100/200, K=500/800/1000, thresholds 1.0/1.5/2.0."
    elif evals_left <= 5:
        return "Final submissions: consolidate best parameters from prior evaluations."
    elif evals_left <= 10:
        return "Diversify: try different selection strategies (top-K vs. ratio threshold)."
    else:
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
