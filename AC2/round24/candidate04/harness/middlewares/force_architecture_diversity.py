"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get('iteration', 0)
    improvement = hook_input.get('improvement_count', 0)
    
    if iteration % 7 == 0 and iteration > 0 and improvement < 1:
        return 'STUCK ALERT: You have been stuck for 7 iterations. CALL explore_architectures or reinitialize_with_architectures to generate new function classes. DO NOT just tune parameters.'
    
    if iteration >= 20 and improvement == 0:
        return 'FINAL ESCAPE: Try completely new architectures (bimodal, piecewise-linear, triangular). Parameter tuning has failed.'
    
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
