"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    probes_used = hook_input.get('probes_used', 0)
    
    if tool == 'evaluate_solution' and probes_used < 4:
        return 'Warning: Call probe_solution on at least 4 variants before full eval to ensure pattern quality.'
    
    if probes_used >= 25 and tool not in ['finish', 'scan_step_patterns']:
        return 'Budget alert: 5 probes left. Evaluate a strong pattern variant soon.'
    
    if iteration <= 12 and 'pattern' not in hook_input.get('tool_name', '').lower() and iteration % 3 == 0:
        return 'Iteration reminder: Consider trying a new step pattern from patterns 0-11.'
    
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
