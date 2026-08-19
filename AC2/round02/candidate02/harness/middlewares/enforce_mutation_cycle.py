"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    last_action = state.get("last_action", "")
    iteration = state.get("iteration", 0)
    
    if last_action == "evaluate" or last_action == "probe":
        if iteration > 0 and iteration % 2 == 0:
            return "MUTATION_REQUIRED: Call struct_mutate before the next evaluation."
    
    if iteration > 0 and iteration % 3 == 0 and last_action != "mutate":
        return "PROBE_BEFORE_EVAL: Use probe_solution to rank variants before evaluate_solution."
    
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
