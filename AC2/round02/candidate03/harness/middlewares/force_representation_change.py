"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    best_score = state.get("best_score", 0)
    last_score = state.get("last_score", 0)
    iterations = state.get("iteration", 0)
    recent_scores = state.get("recent_scores", [])
    
    # Check for plateau: 5+ iterations with minimal improvement
    if iterations >= 5 and len(recent_scores) >= 5:
        for s in recent_scores:
            if s > last_score + 0.001:
                break
        else:
            # Truly plateaued - force structural change
            recent_classes = state.get("recent_classes", [])
            if len(recent_classes) >= 3:
                # Suggest trying a different class
                other_classes = ["step", "Gaussian", "exponential", "B-spline", "Fourier"]
                for cls in other_classes:
                    if cls not in recent_classes:
                        return f"REPRESENTATION_CHANGE_REQUIRED: Recent performance plateaued. Try {cls} functions instead of piecewise-linear. Use scan_function_space to confirm representation, then probe 5-10 variants before evaluation."
            else:
                return "PLATEAU_DETECTED: Scores stable for 5+ iterations. Strongly consider changing the function REPRESENTATION (not just parameters). Use scan_function_space to identify alternatives."
    
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
