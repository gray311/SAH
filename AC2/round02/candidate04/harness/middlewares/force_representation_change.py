"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    best_score = state.get("best_score", 0)
    evals_used = state.get("evals_used", 0)
    recent_scores = state.get("recent_scores", [])
    
    # Check if we've used many evals without structural change
    if evals_used >= 8:
        return "WARNING: You've used 8+ evaluations. Are you still tuning the SAME function representation? If yes, CHANGE to a different class immediately (step functions, Gaussian mixtures, etc.). Probes should have told you which class is promising."
    
    # Check for stagnation
    if len(recent_scores) >= 6:
        if all(s <= best_score + 1e-5 for s in recent_scores):
            return "STAGNATION_DETECTED: You haven't improved in 6+ iterations. This suggests you're over-tuning a single representation. SWITCH to a completely different function class using probe_solution to explore new options."
    
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
