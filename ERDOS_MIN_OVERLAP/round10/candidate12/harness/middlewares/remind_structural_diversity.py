"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_score = hook_input.get("current_score", 0)
    best_score = hook_input.get("best_score", 0)
    iterations = hook_input.get("iteration", 0)
    if iterations > 10 and best_score - current_score < 0.001:
        return "You've been stuck at the same score for 10+ iterations. Call generate_erdos_constructs to get fundamentally NEW structural patterns, not just parameter tweaks. The problem requires structural innovation."
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
