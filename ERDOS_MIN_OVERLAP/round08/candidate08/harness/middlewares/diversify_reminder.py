"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_score = hook_input.get("current_combined_score", 0.0)
    best_score = hook_input.get("best_combined_score", 0.0)
    if current_score < 1.0 and best_score <= 0.999641 + 0.001:
        return "ALERT: Stuck at seed-level (~0.999641). USE struct_generate_candidates NOW to create programs with DIFFERENT structures: step functions, sinusoidal patterns, piecewise-constant, genetic algorithms, or simulated annealing. Generate 3-5 diverse candidates, evaluate top 2-3, refine the winner. Gradient descent is trapped - you need new ansatz families."
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
