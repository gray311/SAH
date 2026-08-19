"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    if len(history) == 0:
        return "FIRST STEP: Generate 3-5 DIVERSE step function constructions from scratch (bipartite, multi-peak, Golomb-ruler, etc.) before any optimization. Use exact formulas. Do NOT start with structural mutations."
    recent_tools = [turn.get("tools_used", []) for turn in history[-3:]]
    has_generated = any("edit_solution" in tools and "correlation_analyzer" not in tools for tools in recent_tools)
    if not has_generated:
        return "REMINDER: You have not yet generated diverse constructions. Create 3-5 different step function shapes first (bipartite, three-peak, Golomb-ruler, etc.). Call edit_solution for each with a COMPLETELY DIFFERENT construction."
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
