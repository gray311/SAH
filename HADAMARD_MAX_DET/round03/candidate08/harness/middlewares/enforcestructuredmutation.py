"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_best = hook_input.get('best_score', 0)
    last_score = hook_input.get('last_score', 0)
    iterations = hook_input.get('iterations', 0)
    
    # Trigger structured mutation advice if stalled
    if iterations > 50 and current_best < 0.48:
        return "🚨 STALLED DETECTED! SA hasn't improved in 5+ evals at score < 0.48. MUST call block_mutation_scramble to escape local optima. Try: row flips, subblock swaps, or column cycles."
    elif iterations > 30 and last_score < 0.50:
        return "⚠️ Approaching plateau. Consider calling block_mutation_scramble after next SA run to explore new regions."
    elif current_best < 0.48:
        return "📊 Low score detected (< 0.48). SA may be stuck. Add block_mutation_scramble to your strategy for diversification."
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
