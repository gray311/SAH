"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get("iteration", 0)
    evals_used = hook_input.get("evals_used", 0)
    
    reminder = None
    
    if iteration >= 10 and evals_used < 15:
        reminder = "You've done 10+ iterations with <15 evals. Are you using probe_solution to filter? Generate 10-12 mutations, probe all, then evaluate top 3-5."
    
    if iteration >= 25:
        reminder = "You've done 25+ iterations. Have you exhausted step-pattern refinements? If yes, try hybrid patterns. Only use non-step families as LAST RESORT."
    
    return reminder
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
