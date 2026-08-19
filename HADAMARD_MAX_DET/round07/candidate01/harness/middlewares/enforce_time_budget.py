"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get('code', '')
    
    # Check for Bareiss - CRITICAL
    if 'bareiss' in code.lower():
        if 'numpy.linalg.det' not in code:
            return "🚨 CRITICAL: Bareiss detected without numpy fallback! This will cause TIMEOUT. Use numpy.linalg.det for all search determinants."
    
    # Check iteration budget
    import re
    iters_matches = re.findall(r'\d+(?:,\d+)*\s*(?:iters?|iterations?)', code)
    if iters_matches:
        total_iters = 0
        for m in iters_matches[:10]:
            num_str = re.sub(r'[,\s]', '', m)
            if num_str.isdigit():
                total_iters += int(num_str)
        
        if total_iters > 1000000:
            return "⚠️ WARNING: >1M total iterations may exceed 180s budget. Reduce seeds or iterations per seed."
    
    # Check time estimate comment
    if '350' in code and '180' not in code:
        return "⚠️ TIP: Your code mentions 350s budget but recommended limit is 180s. Consider reducing iterations."
    
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
