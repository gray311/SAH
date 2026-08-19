"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool_name = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    probes_used = hook_input.get('probes_used', 0)
    evals_used = hook_input.get('evals_used', 0)
    
    if tool_name == 'evaluate_solution' and probes_used < 5:
        return "CRITICAL: Use probes to filter variants first! Only 5+ probes used."
    
    if probes_used > 20 and tool_name == 'probe_solution':
        return "PROBE BUDGET CRITICAL: Only ~8 probes left. Evaluate a promising variant soon."
    
    if evals_used > 15 and tool_name == 'edit_solution':
        return "HALF BUDGET USED: Only 12 full evaluations remaining. Focus on final iterations."
    
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
