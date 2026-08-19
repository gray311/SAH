"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_tool(hook_input):
    iteration = hook_input.get("iteration", 0)
    tool_name = hook_input.get("tool_name", "")
    
    # Prevent architectural jumps
    if tool_name == "edit_solution":
        if "Gaussian" in hook_input.get("context", "") or "B-spline" in hook_input.get("context", ""):
            return "Warning: Don't try Gaussian/B-spline! Use parameter perturbations within step functions only."
    
    # Encourage analysis before generation
    if tool_name == "generate_step_variants":
        return "Reminder: Call analyze_step_structure first to understand current parameters!"
    
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
