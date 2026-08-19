"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    code = hook_input.get('code', '')
    import re
    # Extract iteration counts
    iters = re.findall(r'\d+\s*(?:iters?|iterations?|iters?_per)', code, re.IGNORECASE)
    total_iters = sum(int(i.strip()) for i in iters)
    # Check if total iterations would exceed budget
    # Rough estimate: 29x29 det = 0.001s, so 100k iters = 100s
    estimated_time = total_iters * 0.0001  # conservative estimate
    if estimated_time > 240:
        return f"⚠️ WARNING: Estimated time {estimated_time:.0f}s exceeds 240s budget. Reduce iterations or parallelize fewer searches."
    # Check for Bareiss during search
    if 'bareiss' in code.lower():
        if 'numpy.linalg.det' not in code:
            return "❌ ERROR: Bareiss determinant used without numpy.linalg.det fallback. This will cause timeout."
    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def before_tool(self, hook_input):
        try:
            note = before_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
