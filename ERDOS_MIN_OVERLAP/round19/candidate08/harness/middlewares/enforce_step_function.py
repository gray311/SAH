"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    last_edit = state.get("last_tool_name", "")
    
    reminder = ""
    
    if last_edit == "edit_solution":
        reminder = (
            "After editing, verify the EVOLVE-BLOCK now contains a step-function generator,\
            not gradient descent on sigmoid curves.\
            \nCheck for: N_intervals loops, breakpoint definitions, level assignments.\
            \nDo NOT keep training loops - they waste evals."
        )
    elif "evals_left" in state and state["evals_left"] >= 2:
        reminder = (
            f"{state['evals_left']} evals remaining.\
            \nUse generate_step_candidates with NEW structural parameters (different N, new breakpoint grids).\
            \nDon't repeat the same candidate structure."
        )
    
    return reminder if reminder else None
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
