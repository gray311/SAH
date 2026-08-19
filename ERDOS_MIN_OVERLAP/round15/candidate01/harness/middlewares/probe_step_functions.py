"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    probes_left = state.get("probes_left", 0)
    evals_left = state.get("evals_left", 0)
    
    if probes_left > 10:
        return (
            "You have probes remaining. Use probe_solution to screen step function candidates.\n"
            "Edit seed to use a step function, then probe before calling evaluate_solution.\n"
            "Only spend full evaluations on candidates with probe C5 < 0.375.\n"
            "You have 30 probes total - use them efficiently."
        )
    elif probes_left > 0 and evals_left > 3:
        return (
            "Use remaining probes to screen new step function candidates.\n"
            "Don't waste full evaluations until probe confirms C5 < 0.375."
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
