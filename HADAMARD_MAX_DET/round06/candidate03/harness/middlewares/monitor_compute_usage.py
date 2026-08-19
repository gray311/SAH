"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    if 'bareiss' in code.lower():
        return "WARNING: Bareiss detected! MUST use numpy.linalg.det for search phase."
    import re
    iters = re.findall(r'\d+,?\s*iters?\s*[=:]?\s*\d+', code)
    total = 0
    for m in iters:
        nums = re.findall(r'\d+', m)
        for n in nums:
            total += int(n)
    if total > 500000:
        return "WARNING: >500k iterations may timeout. Reduce iterations."
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
