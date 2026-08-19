"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_left = state.get("evals_left", 0)
    probes_used = state.get("probes_used", 0)
    
    if evals_left >= 4 and probes_used < 1:
        return (
            "You have 4+ evals left and haven't probed yet.\\n"
            "Call generate_many_candidates to get 12 candidates.\\n"
            "Evaluate 3-5 with c5_bound < 0.36.\\n"
            "Don't stop after 1 batch - generate new patterns!"
        )
    elif evals_left >= 2:
        return (
            f"2 evals left. Use them wisely.\\n"
            "Look for c5_bound < 0.35 candidates for full eval.\\n"
            "Consider trying temperature=0.9 for more diversity."
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
