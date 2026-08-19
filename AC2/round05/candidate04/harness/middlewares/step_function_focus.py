"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    evals_done = state.get("evals_done", 0)
    probes_since_eval = state.get("probes_since_eval", 0)
    
    # Enforce generate_variants before edit
    if iteration > 0 and "edit_solution" in str(hook_input.get("action", "")):
        return "REMINDER: Call generate_variants before edit_solution to get concrete mutation suggestions."
    
    # Enforce probe before eval discipline
    if evals_done >= 2 and probes_since_eval < 3:
        return "WARNING: You've done evals without probing. Call probe_solution 3-5 times per edit to properly rank variants."
    
    # Encourage step function focus early
    if iteration <= 5:
        return "STRATEGY HINT: Start with finer discretization (400->1000 intervals) or 3-level step functions. These are theoretically promising for C2."
    
    # Encourage strategy rotation
    if evals_done >= 4 and probes_since_eval >= 5:
        return "STALLED AFTER 4 EVALS: Call generate_variants and switch to a NEW strategy."
    
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
