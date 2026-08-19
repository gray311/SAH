"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    probes_left = state.get("probes_left", 0)
    evals_left = state.get("evals_left", 0)
    
    if probes_left >= 5 and evals_left >= 3:
        return (
            "PROBE FIRST: You have probes available. Probe all new candidates\n"
            "before calling evaluate_solution. Do not call evaluate_solution\n"
            "until you've probed at least 3-5 candidates.\n"
            "Use probes to find c5_bound < 0.37 before spending evaluations."
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
