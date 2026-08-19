"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    probes_left = state.get("probes_left", 0)
    
    if evals_left > 0 and probes_left > 0:
        return (
            "CRITICAL: Call probe_solution FIRST before evaluate_solution!\n"
            "Use probe_solution to screen h(x) candidates.\n"
            "Only call evaluate_solution if probe shows c5_bound < 0.37 and integral ~ 1.\n"
            f"Remaining: {probes_left} probes, {evals_left} evals."
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
