"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    budget_left = state.get("budget_left", 30)
    evals_used = state.get("evals_used", 0)
    last_probe = state.get("last_probe_c5", None)
    last_eval = state.get("last_eval_result", None)
    
    if last_eval is not None and evals_used < budget_left - 5:
        return (
            "You have enough budget left to explore more.\n"
            "Before spending another eval, call probe_solution to screen edits.\n"
            "Only evaluate if probe shows c5_bound < 0.375.\n"
            f"Last probe c5_bound: {last_probe}\n"
            "If last probe was >= 0.375, EDIT EVOLVE-BLOCK and try again.\n"
            "Don't waste evals on configs that probe didn't screen."
        )
    elif last_probe is not None and last_probe >= 0.375:
        return (
            "Last probe returned c5_bound >= 0.375. This config is unlikely to improve.\n"
            "EDIT EVOLVE-BLOCK to change hyperparameters or add new patterns.\n"
            "Try: different num_intervals, learning rate, or new initialization patterns.\n"
            "Then probe again before evaluating."
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
