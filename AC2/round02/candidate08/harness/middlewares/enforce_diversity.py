"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    recent_reps = state.get("recent_representations", [])
    iterations = state.get("iteration", 0)

    if iterations >= 5 and len(recent_reps) >= 5:
        last_repr = recent_reps[-1] if recent_reps else "unknown"
        same_count = sum(1 for r in recent_reps[-5:] if r == last_repr)
        if same_count >= 4:
            return "DIVERSITY_WARNING: Used {} for {} consecutive iterations. Likely local optimum. Use scan_representations to probe other classes or try variants of different class.".format(last_repr, same_count)
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
