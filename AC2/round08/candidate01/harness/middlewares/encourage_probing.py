"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "unknown")
    probes_used = state.get("probes_used", 0)
    evals_used = state.get("evals_used", 0)
    
    # If about to evaluate but haven't probed enough
    if last_tool == "evaluate_solution" and evals_used > 0 and probes_used < 3:
        return "Remember: Use probe_solution for 5-10 variants before evaluating. This saves your expensive eval budget. probe_solution is ~10s and separate budget."
    
    # If many evals used, encourage more probing
    if last_tool == "evaluate_solution" and evals_used >= 5 and probes_used < 5:
        return "WARNING: You've used 5+ evals with limited probing. Consider using more probe_solution calls (~10s each) to rank variants cheaply before next eval."
    
    # Track probes
    if last_tool == "probe_solution":
        probes_used += 1
        state["probes_used"] = probes_used
    
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
