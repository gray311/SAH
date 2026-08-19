"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    history = hook_input.get("history", [])
    
    # If no construct_step_function calls yet, remind
    has_construct = any("construct_step_function" in str(turn.get("tools_used", [])) 
                      for turn in history)
    if not has_construct:
        return "Reminder: Use construct_step_function to create structured step functions (bipartite, bimodal, trimodal, sparse) with integral=1. Avoid random sigmoid-based approaches."
    
    # If we've only tried one structure type, encourage diversity
    structures_tried = set()
    for turn in history:
        if "construct_step_function" in str(turn.get("tools_used", [])):
            tool_result = turn.get("tool_outputs", {}).get("construct_step_function", {})
            if isinstance(tool_result, dict) and "structure" in tool_result:
                structures_tried.add(tool_result["structure"])
    
    if len(structures_tried) <= 1:
        return f"You've only tried {len(structures_tried)} structure type(s). Try different structures: bipartite, bimodal, trimodal, or sparse to explore diverse solutions."
    
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
