"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    family_streak = state.get("family_streak", 0)
    
    if iteration >= 5 and family_streak >= 5:
        families_explored = state.get("families_explored", [])
        if len(families_explored) < 3:
            return "DIVERSIFICATION_STALLED: You've been exploring the same function family for 5 iterations. Call representational_probe and switch to a DIFFERENT function family (not parameter tuning of the same one). Use probe_solution to test 8+ variants of a new family before evaluating." 
        elif len(families_explored) >= 3:
            return "DIVERSIFICATION_STALLED: You've explored 3+ families but not improved. Re-examine your strategy - are you tuning or exploring? Switch to a completely different function class."
    
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
