"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    best_score = hook_input.get("best_combined_score", None)
    evals_left = hook_input.get("evals_left", None)
    
    if iteration <= 2:
        return "Early search: Generate DIVERSE patterns across all classes (single_peak, multi_peak, plateau, staircase, asymmetric, pyramid). Do not focus on one pattern type yet. Use generate_pattern_variants with variety='diverse'."
    elif evals_left and evals_left > 20:
        return "You have many evals left. Generate patterns with varied interval counts (300-800) and different structural families. Probe rank before evaluating."
    elif iteration >= 40:
        return "Late search: Try focused pattern generation. If you have not found a pattern > 1.03492, your strategy needs fundamental change. Consider completely different pattern classes."
    else:
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
