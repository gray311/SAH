"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    last_c5 = state.get("last_probe_c5", None)
    
    if last_c5 is not None and last_c5 >= 0.38:
        return "Previous probe gave c5 >= 0.38 (>= seed). Generate a NEW pattern edit with different structure."
    elif evals_left >= 3 and last_c5 is None:
        return "You haven't probed yet. Generate and probe candidate patterns first. Don't evaluate immediately."
    elif evals_left <= 2 and last_c5 < 0.37:
        return f"Only {evals_left} evals left and last probe c5={last_c5}. If this is best, evaluate now, then finish."
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
