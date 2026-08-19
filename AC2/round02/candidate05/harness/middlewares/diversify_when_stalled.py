"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    best_score = state.get("best_score", 0)
    last_score = state.get("last_score", 0)
    iterations = state.get("iteration", 0)
    
    # Check if we've plateaued for 5+ iterations
    if iterations >= 5:
        recent_scores = state.get("recent_scores", [])
        if len(recent_scores) >= 5:
            if all(s <= last_score + 1e-4 for s in recent_scores):
                return "BEST_SCORE_STALLED: Try a different function representation (step → Gaussian, piecewise-linear → B-spline, etc.) instead of parameter tuning. Use probe_solution to explore new candidates."
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
