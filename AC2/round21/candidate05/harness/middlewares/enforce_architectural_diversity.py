"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    evals_used = hook_input.get('evals_used', 0)
    
    # Warn if not trying diverse interval counts
    if iteration > 5 and evals_used < 3:
        return 'Diversity reminder: Try varying interval counts (200/400/800/1200) or peak configurations.'
    
    # Enforce probe discipline
    if tool == 'evaluate_solution' and evals_used < 5:
        return 'Early iteration: Ensure you have probed multiple variants before this eval.'
    
    # Alert on evaluation budget
    if evals_used >= 25:
        return 'Warning: Only 5 evaluations left. Ensure this is your best variant.'
    
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
