"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    current_code = hook_input.get("current_code", "")
    if 'jax.nn.sigmoid' in current_code or 'jnp.sigmoid' in current_code:
        return None
    if 'jax.nn' in current_code and 'sigmoid' not in current_code:
        return "🔧 Remember: sigmoid(latent) maps to [0,1]. Don't change activation!"
    return "⚠ Check: sigmoid activation and FFT must be preserved. Only tune hyperparameters."
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
