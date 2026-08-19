"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    edits_made = state.get("edits_made", 0)
    evals_left = state.get("evals_left", 0)
    probes_left = state.get("probes_left", 0)
    if edits_made > 0 and evals_left > 0 and probes_left > 0:
        return (
            "Edit the seed with num_restarts=1 to test ONE pattern at a time.\n"
            "Do not set num_restarts>1 unless explicitly testing multiple patterns.\n"
            "Use probe_solution to screen many single-pattern candidates quickly.\n"
            "Only call evaluate_solution on the BEST single-pattern candidate."
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
