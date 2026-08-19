"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    consecutive_same_space = hook_input.get("consecutive_same_space", 0)
    if consecutive_same_space >= 3:
        spaces = ["fourier", "laguerre", "variational", "hermite", "dense_sparse"]
        current = hook_input.get("current_space", "")
        idx = spaces.index(current) if current in spaces else 0
        next_space = spaces[(idx + 1) % len(spaces)]
        return "SWITCH TO NEW FUNCTION SPACE: " + next_space.upper() + ". You've exhausted " + current + " after 3 evals. Do not refine the same type."
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
