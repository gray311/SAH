"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    probes_used = state.get("probes_used", 0)
    best_score = state.get("best_score", 0.999968)
    current_iteration = state.get("iteration", 0)
    
    # If we've done multiple evals without improvement, suggest mutations
    if evals_left >= 2 and current_iteration > 3:
        return (
            f"Best score so far: {best_score:.6f}. "
            "Consider calling analyze_results to get hyperparameter mutations. "
            "Try num_intervals=1000, learning_rate=0.004, penalty_strength=80. "
            "Don't keep generating similar candidates!"
        )
    
    # Early exploration
    if evals_left >= 5 and probes_used < 1:
        return (
            f"Evals left: {evals_left}. "
            "Use probe_solution to rank candidates before full eval. "
            "Call generate_10_candidates with temperature=0.9 for diversity."
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
