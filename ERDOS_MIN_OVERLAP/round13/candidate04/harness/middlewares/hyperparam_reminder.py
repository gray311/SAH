"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    probes_left = state.get("probes_left", 0)
    evals_left = state.get("evals_left", 0)
    if probes_left > 8 and evals_left > 1:
        return (
            "You have many probes remaining. Use them to screen hyperparameter combinations.\n"
            "Create EDIT versions with different penalty_strength, num_intervals, num_steps.\n"
            "Call probe_solution on each to find c5_bound < 0.375 before spending full evaluations.\n"
            "Only call evaluate_solution on the top 3-5 probe-passing candidates.\n"
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
