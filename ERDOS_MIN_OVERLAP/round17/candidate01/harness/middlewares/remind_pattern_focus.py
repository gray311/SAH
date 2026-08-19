"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    evals_used = state.get("evals_used", 0)
    
    if evals_used > 0 and evals_used < 5:
        return (
            "Focus on pattern 12 (Golomb) or 14 (Tri-modal) first.\n"
            "Use pattern_modifier to create variants with adjusted peak widths/thresholds.\n"
            "Small modifications (mod_value=0.5-0.8) are safest.\n"
            "EDIT the EVOLVE-BLOCK with new parameters, then evaluate."
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
