"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_done = state.get("evals_done", 0)
    recent_calls = state.get("recent_calls", [])
    last_call = recent_calls[-1] if recent_calls else None
    families_explored = state.get("families_explored", [])

    if last_call not in ["probe_solution"] and evals_done < 3:
        return "CALL variant_generator FIRST to get variants before editing or evaluating."

    if evals_done >= 3 and iteration >= 15:
        return "STALLED: Try a DIFFERENT function family. Call variant_generator with family='gaussian'|'bspline'|'exponential'."

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
