"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    if tool == 'evaluate_solution':
        return 'REMINDER: Have you called probe_solution for this variant first? Use the 30-probe budget to rank before spending full evaluations!'
    return None

def after_tool(hook_input):
    tool = hook_input.get('tool_name', '')
    if tool == 'probe_solution':
        probe_count = hook_input.get('probe_count', 0)
        remaining = 30 - probe_count
        if remaining > 0:
            return f'Probes remaining: {remaining}. Use them to rank other proposals before full evaluation!'
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
