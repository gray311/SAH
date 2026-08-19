"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    families_tried = state.get("families_tried", [])
    last_family = state.get("last_family", "none")
    evals_done = state.get("evals_done", 0)
    probes_since_last_eval = state.get("probes_since_eval", 0)
    
    # Enforce step function priority
    if len(families_tried) == 0:
        return "PRIORITY: Start with STEP functions (record holders at 0.8963 C2). Call mutation_probe with step function variants first."
    
    # Probe-before-eval enforcement
    if evals_done >= 2 and probes_since_last_eval < 3:
        return "STRICT RULE: You must call probe_solution at least 5 times before any evaluate_solution. Do not evaluate yet!"
    
    # Family diversity enforcement  
    if iteration >= 20 and len(families_tried) < 2:
        return "DIVERSITY ALERT: You've done 20+ iterations on one family. Call mutation_probe and switch to a DIFFERENT function family."
    
    # Stagnation detection
    current_score = state.get("current_score", 0)
    if current_score < 1.02665 and iteration >= 30:
        return "STALLED: Score hasn't exceeded 1.02665 after 30+ iterations. Analyze with c2_analyzer and switch families."
    
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
