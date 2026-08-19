"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_family = state.get("last_family", "none")
    families_count = state.get("families_count", 0)
    
    # Must try steps first
    if iteration < 10 and "step" not in str(last_family).lower():
        if last_family != "none":
            return "Remember: Step functions are the record holders! Prioritize them in your mutation_probe calls."
    
    # Track family exploration
    if iteration % 5 == 0 and families_count < 3:
        return "Progress Check: Ensure you've explored 3+ different function families. Cover step, piecewise, gaussian, exponential."
    
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
