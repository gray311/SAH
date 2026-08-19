"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    iteration = hook_input.get('iteration', 0)
    tool = hook_input.get('tool_name', '')
    
    if iteration <= 5 and 'pattern' not in tool.lower():
        return 'Early iterations: Focus on generating diverse pattern families, not small tweaks.'
    
    if iteration >= 13 and 'probe' in tool.lower():
        return 'Phase 2: Try adding/removing peaks or adjusting height ratios significantly.'
    
    if iteration >= 23:
        return 'Phase 3: Aggressively explore 3-4 peak configurations and concentrated patterns.'
    
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
