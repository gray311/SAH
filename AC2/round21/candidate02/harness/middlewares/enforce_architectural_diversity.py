"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    iteration = hook_input.get('iteration', 0)
    templates_used = hook_input.get('templates_used', [])
    probes_used = hook_input.get('probes_used', 0)
    
    # Ensure we're not using same template twice in Phase 1
    if iteration <= 12 and tool == 'synthesize_step_function':
        if len(templates_used) >= 6:
            return 'Diversity warning: You have used 6 templates. Consider different architectures.'
        templates_used.append(tool)
    
    # Ensure probe usage before eval
    if tool == 'evaluate_solution' and probes_used < 3:
        return 'Budget reminder: Call probe_solution on at least 3 variants before full eval.'
    
    if probes_used >= 20 and iteration <= 15:
        return 'Probe budget alert: You have 10 probes left. Evaluate a promising variant soon.'
    
    if iteration >= 15 and 'reinitialize' not in tool:
        return 'Iteration 15+: Consider structure-hop templates if no improvement.'
    
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
