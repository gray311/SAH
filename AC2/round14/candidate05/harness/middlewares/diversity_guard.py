"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get('iteration', 0)
    last_family = hook_input.get('last_family', 'unknown')
    
    if iteration > 0 and iteration % 8 == 0:
        return 'DIVERSITY CHECK: You are at iteration ' + str(iteration) + '. Have you explored completely different function families in the past 8 iterations? Try new architectures (wavelets, RBFs, custom kernels, etc.) if you have been refining the same type.'
    elif iteration >= 12:
        return 'You have done many iterations. Ensure you are exploring DIVERSE function families, not just variations of one type.'
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
