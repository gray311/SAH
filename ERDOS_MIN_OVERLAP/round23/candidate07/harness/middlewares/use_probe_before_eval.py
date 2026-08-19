"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get('state', {})
    probes_left = state.get('probes_left', 0)
    evals_left = state.get('evals_left', 0)
    pending_evals = state.get('pending_evals', 0)
    if pending_evals > 0 and probes_left >= 1 and evals_left > 0:
        return (
            f"You have {evals_left} evaluations left and {probes_left} probes remaining.\n"
            "Before calling evaluate_solution, MUST call probe_solution first to screen.\n"
            "Only evaluate if probe c5 < 0.37 and integral ~ 1.0.\n"
            "This saves precious eval budget."
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
