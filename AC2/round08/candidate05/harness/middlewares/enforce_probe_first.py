"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "unknown")
    probes_since_eval = state.get("probes_since_eval", 0)
    
    # Warn if evaluating without recent probing
    if last_tool in ["edit_solution", "analyze_step_structure"] and probes_since_eval == 0:
        return "You made an edit but haven't probed yet! Call probe_solution on at least 2-3 variants before evaluating to rank them."
    
    # Require 3+ probes before eval after an edit
    if probes_since_eval < 3 and last_tool not in ["probe_solution", "evaluate_solution", "finish"]:
        return "Best practice: Probe 3-5 variants before evaluating. This helps you pick the most promising candidate."
    
    # Reset counter after probe
    if last_tool == "probe_solution":
        state["probes_since_eval"] = probes_since_eval + 1
    elif last_tool == "evaluate_solution":
        state["probes_since_eval"] = 0
    
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
