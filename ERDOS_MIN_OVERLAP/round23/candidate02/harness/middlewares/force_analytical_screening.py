"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    action = hook_input.get("action", {})
    
    # Check if trying to evaluate without screening
    if action.get("tool_call") == "evaluate_solution":
        if "screened_candidates" not in state:
            return (
                "ERROR: You must CALL compute_analytical_c5 first!\\n"
                "Generate candidates, screen with compute_analytical_c5,\\n"
                "only then evaluate candidates with c5_bound < 0.37.\\n"
                "Do NOT call evaluate_solution without screening."
            )
    
    # Remind to screen remaining patterns
    patterns_left = state.get("patterns_left", 15)
    if patterns_left > 0 and "evaluated_count" not in state:
        return (
            f"Patterns remaining: {patterns_left}\\n"
            "Use compute_analytical_c5 to screen each pattern.\\n"
            "Only evaluate if c5 < 0.37."
        )
    
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
