"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    eval_budget = hook_input.get('evaluations_left', 20)
    probe_budget = hook_input.get('probes_left', 30)
    if eval_budget > 0 and eval_budget < 15:
        return f"Low eval budget ({eval_budget} left)! Use {probe_budget} probes to rank variants before spending evaluations."
    elif probe_budget > 20:
        return f"Plenty of probes ({probe_budget} left). Use probe_solution to test multiple algorithmic approaches before full evaluation."
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
