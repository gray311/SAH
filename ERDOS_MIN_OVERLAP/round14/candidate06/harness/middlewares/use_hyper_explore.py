"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    probes_left = state.get("probes_left", 0)
    if probes_left > 2 and state.get("evals_left", 10) > 2:
        return (
            "Remember: Don't replace the seed's 12 initialization patterns!\n"
            "They already provide good diversity.\n"
            "Instead, use generate_hyper_diversity to vary num_intervals, learning_rate,\n"
            "penalty_strength while keeping num_restarts >= 1.\n"
            "Use probes to screen configs before full evaluation."
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
