"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_used = state.get("evals_used", 0)
    families = state.get("families_explored", [])
    step_exploration = state.get("step_explored", 0)
    
    # Force step exploration in first 6 evals
    if evals_used <= 6 and "step" not in families:
        return "STEP_FUNCTIONS_CRITICAL: The current world record (0.8963) is achieved by step functions. The seed barely explored this class. BEFORE exploring B-splines or Gaussians, generate 3-5 aggressive step function variants using probe_solution. Variants to try: (1) Wide support [0.1,0.9] with 4-5 levels, (2) Asymmetric [0.05,0.6]+[0.4,0.95], (3) 6-level multi-height steps. These are record-holders - test them HARD." 
    
    # Force B-spline introduction by eval 7-10
    elif evals_used <= 10 and len(families) < 3 and "b-spline" not in families:
        return "B-SPLINE_THREAT: Seed barely tested B-splines. If you have only explored piecewise-linear or steps, switch to B-spline representations (100-300 knots). B-splines offer C^k continuity that may concentrate convolution better than sharp steps."
    
    # Warn about stagnation
    elif evals_used > 10 and len(families) < 3:
        return "DIVERSIFICATION_LOW: You have used 10+ evals but explored <3 families. This is too conservative. Switch to an under-explored representation class (B-splines, Gaussians, or exponential)."
    
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
