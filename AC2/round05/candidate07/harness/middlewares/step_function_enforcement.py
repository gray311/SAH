"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_done = state.get("evals_done", 0)
    probes_done = state.get("probes_done", 0)
    last_family = state.get("last_family", "none")
    families = state.get("families_explored", [])
    
    # Enforce probe discipline
    if evals_done >= 2 and probes_done < 5:
        return "CRITICAL: You've evaluated but haven't probed 5+ variants. Call analyze_c2_function and probe before evaluating again."
    
    # Enforce step-function priority
    if iteration < 30:
        return "REMEMBER: Step functions dominate C₂. Focus on piecewise-constant mutations via analyze_c2_function."
    
    # Diversification
    if iteration >= 40 and len(families) < 3:
        return "DIVERSIFY: You've explored <3 families. Call analyze_c2_function with a new function family."
    
    # Evaluation budget protection
    if evals_done >= 5:
        return "WARNING: 5+ evaluations used. You have ~15 evals left. Probe more, evaluate less!"
    
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
