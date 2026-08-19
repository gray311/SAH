"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "unknown")
    used_fourier = state.get("used_fourier", 0)
    evals_used = state.get("evals_used", 0)
    
    # First 2 iterations: allow free exploration
    if iteration < 2:
        return None
    
    # After iteration 2, require Fourier analysis before major edits
    if iteration >= 2 and last_tool == "edit_solution" and used_fourier < 1:
        return "CRITICAL: You're about to make a major edit. Call fourier_space_probe FIRST to understand current spectral properties. This guides which architecture to try next."
    
    # Warn if evaluating without Fourier analysis
    if last_tool == "evaluate_solution" and used_fourier == 0:
        return "WARNING: You're evaluating without Fourier analysis. Did you understand the spectral properties of your function? Consider calling fourier_space_probe first."
    
    # Track Fourier usage
    if last_tool == "fourier_space_probe":
        used_fourier += 1
        state["used_fourier"] = used_fourier
    
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
