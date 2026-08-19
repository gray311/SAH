"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    
    # Check if we're still using the seed's weak optimization
    recent_edits = state.get("recent_edits", [])
    
    if iteration > 5 and len(recent_edits) > 0:
        last_edit = recent_edits[-1].get("edit_type", "")
        if "relu" in last_edit.lower() or "gradient" in last_edit.lower() or "linear" in last_edit.lower():
            return "WARNING: Avoid jax.nn.relu and gradient-based optimization. Use TRUE step functions with jnp.piecewise. Call step_function_builder for code."
    
    # Probe before eval discipline
    evals_done = state.get("evals_done", 0)
    probes_since_last_eval = state.get("probes_since_eval", 0)
    
    if evals_done > 0 and probes_since_last_eval < 5:
        return f"REMINDER: You've done {evals_done} full evaluations but less than 5 probes since the last eval. Call probe_solution 5+ times before evaluating again."
    
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
