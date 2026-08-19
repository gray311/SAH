"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    last_action = hook_input.get("last_action", "")
    if "Gaussian" in last_action or "B-spline" in last_action or "oscillatory" in last_action:
        return "WARNING: Stay in step-function landscape! Generate PERTURBED step patterns, not smooth functions. Step functions achieve the current best (0.8963)."
    if iteration > 5 and "evaluate" in last_action.lower():
        return "Reminder: Have you probed all variants first? Use probes to filter before full eval."
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
