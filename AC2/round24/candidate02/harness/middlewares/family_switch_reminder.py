"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    iteration = hook_input.get('iteration', 0)
    tool_name = hook_input.get('tool_name', '')
    probes_used = hook_input.get('probes_used', 0)
    
    if iteration <= 8 and tool_name != 'scan_function_class':
        return "Reminder: Call scan_function_class to explore function families before evaluating."
    
    if probes_used < 5 and 'evaluate_solution' in tool_name:
        return "Warning: Insufficient probes used. Call scan_function_class or probe_solution first."
    
    if iteration >= 23 and tool_name == 'finish':
        return "Final submission: Ensure c2 > 0.8962799441554086. Report winning family and configuration."
    
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
