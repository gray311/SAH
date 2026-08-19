"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    
    # Check for multi-chain implementation
    if 'chain' in code.lower() and ('6' in code or 'perturbed' in code or 'random' in code):
        return None  # Good: multi-chain detected
    
    # Check for single-chain parameter sweep pattern
    if 'parameter' in code.lower() and 'sweep' in code.lower():
        return "⚠️ Using parameter sweep on single seed may get stuck in local optimum. Try multi-chain diverse initialization instead."
    
    # Check for single SA run
    if 'sa(' in code.lower() and 'range(' not in code.lower():
        return None
    
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
