"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    tool_name = hook_input.get("tool_name", "")
    if tool_name == "evaluate_solution":
        best_score = hook_input.get("best_score", 1.0)
        evals_left = 30 - hook_input.get("evals_used", 0)
        probes_left = 30 - hook_input.get("probes_used", 0)
        return "Have you called probe_solution first? You have " + str(probes_left) + " probes to filter candidates before spending " + str(evals_left) + " evaluations. Only evaluate if probe > " + str(best_score) + "!"
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
