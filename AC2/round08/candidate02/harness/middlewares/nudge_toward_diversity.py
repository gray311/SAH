"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    num_intervals_history = state.get("num_intervals_history", [])
    function_types_history = state.get("function_types_history", [])
    
    # After 15 iterations without interval diversity, suggest change
    if iteration >= 15 and len(num_intervals_history) >= 3:
        unique_intervals = len(set(num_intervals_history))
        if unique_intervals < 2:
            return "Consider trying a different discretization resolution. Current patterns may be stuck in local minima."
    
    # After 10 iterations without function diversity, suggest new representation
    if iteration >= 10 and len(function_types_history) >= 2:
        unique_types = len(set(function_types_history))
        if unique_types == 1 and "step" in function_types_history[0].lower():
            return "Try a completely different function representation: Gaussian mixture, spline, or Fourier basis."
    
    # Nudge toward higher resolution after successful initial optimization
    if iteration >= 30 and num_intervals_history:
        avg_intervals = sum(num_intervals_history) / len(num_intervals_history)
        if avg_intervals < 600:
            return f"Current resolution is low (~{int(avg_intervals)}). Consider increasing to 800-1200 intervals for better accuracy."
    
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
