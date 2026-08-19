"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    probes_used = hook_input.get('probes_used', 0)
    
    if iteration <= 5 and 'recombine' not in tool.lower() and 'analyze' not in tool.lower():
        return 'Early iteration: Focus on pattern recombination (merge/split peaks) before parameter tweaks.'
    
    if probes_used >= 12 and tool == 'probe_solution':
        return 'Budget alert: 18 probes left. Evaluate promising recombination soon.'
    
    if iteration >= 15 and 'gradient' not in hook_input.get('tool_name', ''):
        return 'Iteration 15+: Consider frequency-domain optimization (Phase 2).'
    
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
