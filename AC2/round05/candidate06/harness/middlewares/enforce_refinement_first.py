"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_done = state.get("evals_done", 0)
    last_family = state.get("last_family", "piecewise-linear")
    families_explored = state.get("families_explored", [])

    if "piecewise-linear" in families_explored:
        if evals_done < 3 and last_family == "piecewise-linear":
            return "WARNING: You've only evaluated once on piecewise-linear. Refine intervals, learning rate, or steps first. Don't switch to step functions yet."
        elif evals_done >= 3 and last_family != "piecewise-linear":
            return "CAUTION: You've tried 2+ families. Consider returning to piecewise-linear refinements first - they may yield improvements."

    if last_family not in ["none", "piecewise-linear"]:
        if last_family not in families_explored:
            families_explored.append(last_family)

    if len(families_explored) >= 2 and evals_done >= 5:
        return "DIVERSIFICATION_WARNING: You've explored 2+ families. Return to refining piecewise-linear before more diversification."

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
