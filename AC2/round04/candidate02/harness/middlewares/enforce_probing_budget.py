"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    
    # Track mutation types explored
    family_streak = state.get("family_streak", 0)
    families_explored = state.get("families_explored", [])
    last_family = state.get("last_family", "none")
    
    # Enforce probe before eval discipline
    evals_done = state.get("evals_done", 0)
    probes_since_eval = state.get("probes_since_eval", 0)
    
    if evals_done >= 3 and probes_since_eval < 3:
        return "WARNING: You've evaluated 3+ times but haven't probed since last eval. Call probe_solution 5+ times before evaluating again to ensure proper ranking."
    
    # Enforce family diversity
    if iteration >= 15 and last_family in families_explored:
        if len(families_explored) < 2:
            return "DIVERSIFICATION_WARNING: You've been exploring the same function family. Call mutation_probe and switch to a DIFFERENT mutation type."
        else:
            return "DIVERSIFICATION_WARNING: You've explored 2+ families but no improvement. Re-examine your mutations - are you exploring or tuning? Call mutation_probe for a new family."
    
    # Streak detection
    if family_streak >= 5:
        return "STALLED: You've done 5 iterations on the same mutation type. Call mutation_probe to switch to a different function family or mutation strategy."
    
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
