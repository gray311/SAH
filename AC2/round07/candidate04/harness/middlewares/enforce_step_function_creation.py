"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    
    # Track if step_config_generator was used
    used_step_config = state.get("used_step_config", False)
    last_tool = state.get("last_tool", "unknown")
    
    # After first few iterations, enforce using step_config_generator
    if iteration >= 3 and not used_step_config:
        return "WARNING: You haven't used step_config_generator yet. The seed program uses piecewise-LINEAR optimization but step functions must be PIECEWISE-CONSTANT. Call step_config_generator to get structured step parameters before editing."
    
    # Warn if editing without using step_config_generator output
    if iteration >= 5 and last_tool in ["edit_solution"] and not used_step_config:
        return "WARNING: You edited without using step_config_generator. The seed's linear optimization won't work for step functions. Use step_config_generator first to get TRUE step parameters."
    
    # Track progress
    if last_tool == "step_config_generator":
        state["used_step_config"] = True
    
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
