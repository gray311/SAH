"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    recent_configs = state.get("recent_configs", [])
    
    if len(recent_configs) >= 3:
        # Check for diversity
        step_counts = [c.get("num_steps", 0) for c in recent_configs]
        symms = [c.get("symmetric", True) for c in recent_configs]
        
        # Warn if too similar
        if len(set(step_counts)) == 1 and len(set(symms)) == 1:
            last_num_steps = step_counts[0]
            last_sym = symms[0]
            return f"WARNING: Your last 3 configs all have {last_num_steps} steps and {last_sym}. Create structurally different step functions (vary num_steps: 2,3,4,5 and symmetry)."
        
        # Warn if repeating same pattern
        if len(recent_configs) >= 4:
            if recent_configs[-1] == recent_configs[-3]:
                return "WARNING: Repeating the same step pattern. Create a NEW step function configuration." 
    
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
