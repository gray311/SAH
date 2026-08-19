"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    probes_used = state.get("probes_used", 0)
    if probes_used >= 3 and evals_left >= 2:
        return (
            "Use generate_ready_candidates to get integral-constrained candidates.\n"
            "Only evaluate candidates with c5_bound < 0.37.\n"
            f"You have {evals_left} evals left - use them wisely.\n"
            "Skip candidates with integral != 1.0 or c5_bound >= 0.375."
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
