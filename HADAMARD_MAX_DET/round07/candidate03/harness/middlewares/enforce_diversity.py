"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    
    if 'paley' in code.lower() and 'random' not in code.lower() and 'greedy' not in code.lower():
        return "WARNING: Only using Paley construction! MUST try at least 3 different starting methods per evaluation."
    
    if 'random' in code.lower() and 'paley' not in code.lower() and 'greedy' not in code.lower():
        return "WARNING: Only using random initialization! You should try multiple construction methods per evaluation."
    
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
