"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    import json
    try:
        evals_left = hook_input.get("state", {}).get("evals_left", 20)
        best_score = hook_input.get("state", {}).get("best_score", 1.0)
        iterations = hook_input.get("state", {}).get("iterations", 0)
        stagnation = hook_input.get("state", {}).get("stagnation_count", 0)
        
        if stagnation >= 5 and iterations > 10 and evals_left > 10:
            return "PROGRESS STALLED: Call explore_function_classes with diversity_mode='balanced' and num_candidates=80 to search new function families. Don't keep refining the same pattern."
        elif stagnation >= 3 and iterations > 20 and evals_left > 15:
            return "Consider exploring smooth functions or asymmetric patterns. Try diversity_mode='smooth_only' or diversity_mode='asymmetric_only'."
    except:
        pass
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
