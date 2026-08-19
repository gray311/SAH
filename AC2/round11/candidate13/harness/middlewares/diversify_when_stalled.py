"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    # Check recent iteration context for stagnation
    recent_ctx = hook_input.get("recent_iteration", {})
    last_c2 = recent_ctx.get("last_c2", 0)
    best_c2 = recent_ctx.get("best_c2", last_c2)
    
    if best_c2 == last_c2 and recent_ctx.get("iter_count", 0) > 10:
        return "STALLED: Force new architecture. Use mutator_tool with force_diversity=True"
    
    # Remind to use evaluate over probe
    return "Remember: evaluate_solution only. Probe is unreliable for C2."
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
