"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get('iteration', 0)
    improvement_count = hook_input.get('improvement_count', 0)
    
    if iteration >= 10 and improvement_count < 2:
        return 'WARNING: No improvement after 10 iterations. ESCAPE step-function paradigm - try smooth edges, multi-scale superposition, or Fourier optimization.'
    
    if iteration >= 20 and improvement_count < 5:
        return 'CRITICAL: Still plateaued. AGGRESSIVE ARCHITECTURE SEARCH PHASE - completely rearchitect function class.'
    
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
