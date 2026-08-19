"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    last_family = hook_input.get("last_family", "")
    streak = hook_input.get("family_streak", 0)
    
    # If we've refined the same family for 6+ iterations, force a new family
    if streak >= 6:
        return "WARNING: You've been refining the same family for " + str(streak) + " iterations. This is a local optimum trap. Generate and test candidates from DIFFERENT function families (Gaussian, oscillatory, asymmetric multi-peaked, etc.). Switch to a NEW family immediately."
    
    # At iteration 1, encourage diverse starting point
    if iteration == 1 and "generate_candidates" not in hook_input.get("planned_actions", ""):
        return "START STRATEGY: Call generate_candidates to get diverse proposals from DIFFERENT function families. Do NOT start by refining step functions. Explore Gaussian mixtures, oscillatory functions, and asymmetric multi-peaked architectures first."
    
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
