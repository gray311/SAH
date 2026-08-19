"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def after_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    consecutive_same = hook_input.get('consecutive_same_family', 0)
    family_type = hook_input.get('family_type', 'unknown')

    if tool == 'evaluate_solution' and consecutive_same >= 2:
        msg = f'WARNING: Same family ({family_type}) for {consecutive_same} iterations. Switch with generate_function_family!'
        return msg

    if tool == 'generate_function_family':
        return None

    return None
# --USER-HOOK-END--

class GeneratedMiddleware(Middleware):
    def after_tool(self, hook_input):
        try:
            note = after_tool(hook_input)
        except Exception:
            return HookResult.no_changes()
        if not note:
            return HookResult.no_changes()
        try:
            msg = Message(role=Role.FRAMEWORK, content=[TextBlock(text=str(note)[:2000])])
            return HookResult.with_modifications(messages=[*hook_input.messages, msg])
        except Exception:
            return HookResult.no_changes()
