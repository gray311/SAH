"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_action = state.get("last_action", "")
    
    # Warn against manual step construction
    if "step_function" in last_action.lower() or "replace optimizer" in last_action.lower():
        return "WARNING: DO NOT replace the seed's JAX optimizer! It uses powerful gradient descent over 40,000 steps. Instead, ADD new initialization functions that the optimizer can improve via gradient descent."
    
    # Encourage probing after partial optimization
    if iteration > 5 and "evaluate" in last_action.lower():
        return "REMINDER: You're evaluating without prior probing! Run the optimizer for 1000 steps first, then call probe_solution to rank variants before full evaluation."
    
    # Check for diversity
    families_tried = state.get("families_tried", [])
    if len(families_tried) == 1 and iteration > 10:
        return "DIVERSIFICATION NEEDED: You've only tried one initialization family. Call hybrid_function_creator with different hybrid_type values to explore more function shapes."
    
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
