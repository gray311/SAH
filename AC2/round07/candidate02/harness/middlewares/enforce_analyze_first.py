"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "unknown")
    analyzed = state.get("analyzed", False)
    
    # After first edit, enforce analyze before next edit
    if iteration >= 2 and last_tool == "edit_solution" and not analyzed:
        return "WARNING: You just edited without analyzing the current best first! Call analyze_step_config to understand the function structure before making targeted edits. This enables systematic refinement."
    
    # Warn if many iterations without analysis
    if iteration >= 5 and not analyzed:
        return "WARNING: You haven't called analyze_step_config yet after 5 iterations. The seed program uses piecewise-linear optimization. Call analyze_step_config to extract step parameters and get targeted improvement suggestions."
    
    # Track state
    if last_tool == "analyze_step_config":
        state["analyzed"] = True
    
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
