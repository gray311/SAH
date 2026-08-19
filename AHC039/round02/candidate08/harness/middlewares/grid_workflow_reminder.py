"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    code = hook_input.get("current_code", "")
    recent = hook_input.get("recent_edits", [])
    
    reminder = []
    
    if "analyze_grid" not in code and "unique_x" not in code and "unique_y" not in code:
        reminder.append("Step 1: Extract unique X/Y coords from mackerels")
    
    if "build_polygon" not in code and "bounding_box" not in code and "lshape" not in code:
        reminder.append("Step 2: Build polygon from grid lines")
    
    used_probe = any("probe" in e.get("tool", "").lower() for e in recent[-3:])
    if not used_probe:
        reminder.append("Step 3: Use probe_solution() before evaluate_solution()")
    
    if reminder:
        return "Workflow reminder: " + " -> ".join(reminder) + " Search <0.15s"
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
