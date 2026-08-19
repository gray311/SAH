"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    remaining = hook_input.get("evaluations_left", 0)
    best_score = hook_input.get("best_score", 0)
    if remaining <= 5 and best_score < 1.0:
        return f"⚠️ Only {remaining} evals left! Current best={best_score:.4f}. Need strong move to beat 1.0! Consider: (1) structured step function, (2) simplify then refine, (3) explicit constraint enforcement."
    elif remaining <= 10:
        return f"⚠️ {remaining} evals remaining. Best={best_score:.4f}. Making progress but no guarantees."
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
