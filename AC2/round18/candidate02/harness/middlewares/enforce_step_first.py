"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get('iteration', 0)
    step_mutations_used = hook_input.get('step_mutations_count', 0)
    new_family_used = hook_input.get('new_family_used', False)
    
    if iteration >= 8 and not new_family_used:
        return f'Reminder: Only {step_mutations_used} step mutations used. Generate more step variants before trying Gaussian/spline/oscillatory families. Steps are proven!'
    
    if new_family_used and iteration >= 21:
        return 'You have a new family. Stay focused on it for 5 iterations before trying another.'
    
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
