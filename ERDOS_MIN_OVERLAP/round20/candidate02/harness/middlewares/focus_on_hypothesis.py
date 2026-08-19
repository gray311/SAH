"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    edits_made = state.get("edits_made", 0)
    
    if edits_made < 2 and evals_left >= 5:
        return (
            "You haven't made any edits yet. Call mutate_optimizer to make a targeted hyperparameter edit.\n"
            "Focus on: num_intervals, base_learning_rate, penalty_strength, or latent_bias.\n"
            "Don't try to rewrite the optimizer; tweak existing parameters."
        )
    elif edits_made >= 3 and evals_left >= 2:
        return (
            f"You've made {edits_made} edits. If none improved, try a different parameter.\n"
            "Consider: num_intervals=3200, base_learning_rate=0.003, or adding latent_bias.\n"
            "Use probe_solution to check before full eval."
        )
    elif evals_left >= 1 and edits_made < 5:
        return (
            f"{evals_left} evals left. Make one targeted edit with mutate_optimizer.\n"
            "If you've already tried many params, consider completely different strategies.\n"
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
