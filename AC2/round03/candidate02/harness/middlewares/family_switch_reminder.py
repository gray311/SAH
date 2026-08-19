"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_used = state.get("evals_used", 0)
    best_score = state.get("best_score", 0.0)
    families_explored = state.get("families_explored", [])
    family_history = state.get("family_history", [])
    current_family = "unknown"
    if family_history:
        current_family = family_history[-1].get("family", "unknown")
    if best_score < 1.02649:
        if current_family != "piecewise-constant":
            return "CRITICAL: Best score ({:.3f}) below seed. Switch to step functions (piecewise-constant) immediately. Current family: {}".format(best_score, current_family)
    family_streak = 0
    if family_history:
        for i in range(len(family_history) - 1, -1, -1):
            if family_history[i].get("family") == current_family:
                family_streak += 1
            else:
                break
    if family_streak >= 5:
        return "DIVERSIFICATION_WARNING: Same family for {} evals. Call convolution_analyzer and switch to a different function family.".format(family_streak)
    if evals_used > 10 and best_score < 1.02649:
        return "EVAL_BUDGET_WARNING: Used {} evals without improvement. Call convolution_analyzer and switch families immediately.".format(evals_used)
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
