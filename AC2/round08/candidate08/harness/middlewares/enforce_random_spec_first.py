"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    last_tool = state.get("last_tool", "unknown")
    used_generate = state.get("used_generate", 0)
    
    # First edit must use generate_step_spec
    if iteration >= 1 and last_tool == "edit_solution":
        if used_generate == 0:
            return "CRITICAL: You edited without generating a step spec! Call generate_step_spec FIRST to get a random step configuration (num_steps, boundaries, heights), then edit using that spec."
    
    # Warn if evaluating without generate
    if last_tool == "evaluate_solution" and used_generate == 0:
        return "WARNING: You're about to evaluate without generating a step spec! Did you call generate_step_spec and use its output in your edit?"
    
    # Track generation
    if last_tool == "generate_step_spec":
        used_generate += 1
        state["used_generate"] = used_generate
    
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
