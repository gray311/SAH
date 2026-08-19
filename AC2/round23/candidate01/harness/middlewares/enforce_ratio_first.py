"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    last_ratio_call = hook_input.get('last_ratio_call', -1)
    
    if tool in ['edit_solution', 'probe_solution', 'evaluate_solution'] and iteration < 12:
        if last_ratio_call < iteration - 1:
            return 'Error: You must call analyze_ratio_structure at the start of each iteration before mutating.'
    
    probes_used = hook_input.get('probes_used', 0)
    if probes_used >= 25:
        return 'Critical: Only 5 probes left. Evaluate a promising variant soon.'
    
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
