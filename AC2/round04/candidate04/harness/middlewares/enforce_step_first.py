"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "")
    
    # If we've been iterating on piecewise-linear without trying steps
    if last_tool in ["edit_solution", "probe_solution"] and iteration >= 3:
        program = hook_input.get("program", "")
        if "piecewise-linear" in str(program).lower() and "step" not in str(program).lower():
            return "STEP_FUNCTION_REQUIRED: You've been optimizing piecewise-linear functions. The record-holders (0.8963) use STEP FUNCTIONS. Call create_step_function_variant to generate step function variants immediately. Don't keep tuning piecewise-linear parameters!"
    
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
