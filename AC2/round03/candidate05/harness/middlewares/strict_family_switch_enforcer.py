"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_used = state.get("evals_used", 0)
    evals_remaining = 20 - evals_used
    recent_improvement = state.get("recent_improvement", True)
    last_family = state.get("last_family", "unknown")
    
    if evals_remaining <= 3 and not recent_improvement:
        return "CRITICAL: Only " + str(evals_remaining) + " evals left with no improvement on " + last_family + ". SWITCH to DIFFERENT function family using code_snippet_generator."
    
    if iteration >= 10 and not recent_improvement:
        return "DANGER: Iteration " + str(iteration) + " with no improvement since " + last_family + ". Use code_snippet_generator to switch families. Probe 5+ variants before evaluating next."
    
    if evals_used <= 2 and iteration >= 3:
        return "REMINDER: Few evals used but may be skipping probes. Remember: 5+ probes, max 2 evals per family. Use probe_solution to rank before evaluating!"
    
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
