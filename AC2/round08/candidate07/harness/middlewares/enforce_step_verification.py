"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "unknown")
    used_verify = state.get("used_verify", 0)
    
    # After first edit, require verification
    if iteration >= 2 and last_tool == "edit_solution" and used_verify < 1:
        return "CRITICAL: You edited but haven't verified the step function structure. Call analyze_step_structure immediately to confirm you created TRUE step functions (not linear ramps) before evaluating!"
    
    # Warn if about to evaluate without verification
    if last_tool == "evaluate_solution" and used_verify == 0:
        return "WARNING: You're about to evaluate without verifying step structure. Did you call analyze_step_structure and confirm is_piecewise_constant: True?"
    
    # Track verification attempts
    if last_tool == "analyze_step_structure":
        used_verify += 1
        state["used_verify"] = used_verify
    
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
