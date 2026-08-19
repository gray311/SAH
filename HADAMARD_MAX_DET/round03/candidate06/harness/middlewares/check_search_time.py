"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    # Check for Bareiss during search - CRITICAL FAILURE
    if 'bareiss' in code.lower() and 'numpy.linalg.det' not in code:
        return "🚨 CRITICAL: Bareiss determinant during search will cause TIMEOUT! MUST use numpy.linalg.det for all hill climbing. Bareiss only for final validation."
    # Check iteration count
    import re
    iters = re.findall(r'\d+,?\s*iters?', code)
    if iters:
        total_iters = sum([int(i.replace(',', '')) for i in iters[:5]])
        if total_iters > 800000:
            return "⚠️ WARNING: >800k iterations may exceed 350s. Reduce iterations or parallelize with fewer seeds."
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
