"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    current_function_type = state.get("function_type", "unknown")
    recent_scores = state.get("recent_scores", [])
    
    # Check for piecewise-linear tunneling
    if current_function_type == "piecewise-linear" and iteration >= 8:
        if len(recent_scores) >= 5 and max(recent_scores) <= 1.0265:
            return "HARD_SWITCH_TO_STEPS: You've been optimizing piecewise-linear functions for 8+ iterations without improving beyond 1.0265 (seed baseline + tiny). The record-holder is STEP FUNCTIONS at C2=0.8963. CALL generate_step_variants immediately and switch to step function representations. ABORT the piecewise-linear approach."
    
    # Check for prolonged exploration without step functions
    if iteration >= 15 and "step" not in str(current_function_type).lower():
        return "STILL_NO_STEPS: You're exploring 15+ iterations without testing step functions. The current record (0.8963) is held by step functions. You must test them now. Call generate_step_variants or switch_to_step_functions tool."
    
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
