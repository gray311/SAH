"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    state = hook_input.get("state", {})
    iteration = state.get("iteration", 0)
    configs_tried = state.get("configs_tried", [])
    last_config = state.get("last_config", {})
    
    # Warn if same config repeated
    if last_config and iteration > 1:
        current_config = state.get("current_config", {})
        if current_config == last_config:
            return "REPEATED_CONFIG: You're using the same hyperparameters as before. Generate a new config using hyperparameter_sweeper with a different seed_num."
    
    # Warn if only one config family
    if len(configs_tried) >= 2:
        interval_values = [c.get("num_intervals", 0) for c in configs_tried]
        if len(set(interval_values)) == 1:
            return "SAME_INTERVALS: All configs have the same num_intervals. Generate configs with different num_intervals using hyperparameter_sweeper."
    
    # Probe discipline
    probes_since_eval = state.get("probes_since_eval", 0)
    evals_done = state.get("evals_done", 0)
    if evals_done >= 3 and probes_since_eval < 4:
        return "PROBE_WARNING: You've done 3+ evals but not enough probes. Call probe_solution 4+ times before evaluating again."
    
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
