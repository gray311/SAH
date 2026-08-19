"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    import re
    # Check for Paley construction (bad)
    if 'paley' in code.lower() or 'quadratic_residues' in code.lower():
        return "🚫 CRITICAL: Using Paley construction! You MUST use RANDOM initialization. The seed already uses Paley - you need a DIFFERENT approach."
    # Check for random initialization (good)
    if 'random' in code.lower() and ('randint' in code.lower() or 'choice' in code.lower()):
        return "✅ Good: Using random initialization"
    # Check for np.array with random values
    if 'np.random' in code.lower():
        return "✅ Good: Using numpy random"
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
