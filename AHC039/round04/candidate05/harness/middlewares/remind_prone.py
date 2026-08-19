"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get("code", "")
    tool_history = hook_input.get("tool_history", [])
    
    recent = tool_history[-3:] if tool_history else []
    
    # If editing after edit without probe, remind
    edits = [t for t in recent if "edit" in str(t).lower()]
    probes = [t for t in recent if "probe" in str(t).lower()]
    analyzes = [t for t in recent if "analyze" in str(t).lower()]
    
    if len(edits) >= 2 and len(probes) == 0:
        return "Recent edits made without probing. Use probe_solution first to quickly rank variants before spending full evaluations."
    
    if len(edits) > 0 and len(analyzes) == 0:
        return "Before editing, analyze the current polygon structure. What mutations are most promising?"
    
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
