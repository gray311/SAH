"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_tool(hook_input):
    state = hook_input.get("state", {})
    last_tool = hook_input.get("last_tool", "unknown")
    iterations = state.get("iteration", 0)
    
    # Track evaluation budget
    evals_used = state.get("evals_used", 0)
    probes_used = state.get("probes_used", 0)
    
    if last_tool == "evaluate_solution":
        state["evals_used"] = evals_used + 1
        if evals_used >= 20:
            return "CRITICAL: Evaluation budget exhausted (20/20). Cannot call evaluate_solution anymore."
        elif evals_used >= 15:
            return "WARNING: Using 15/20 evaluations. Be very selective with evaluate_solution."
    
    # Track probe usage
    if last_tool == "probe_solution":
        state["probes_used"] = probes_used + 1
        
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def after_tool(self, hook_input):
        try:
            note = after_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
