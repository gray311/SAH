"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    probes_used = hook_input.get('probes_used', 0)
    patterns_used = hook_input.get('patterns_used', [])
    
    if tool == 'evaluate_solution' and probes_used < 4:
        return 'Critical: Probe at least 4 diverse architectures before full eval.'
    
    if iteration <= 12 and probes_used >= 3 and len(patterns_used) < 3:
        return 'Reminder: Ensure 3+ different pattern types in probes.'
    
    if iteration >= 15 and probes_used < 2:
        return 'Iteration 15+: Probe aggressively before eval. Use gen_step_config for new patterns.'
    
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
