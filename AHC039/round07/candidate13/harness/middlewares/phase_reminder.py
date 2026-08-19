"""Generated middleware (h2spec/1.0) — wrapped, fail-open."""
from nexau.archs.main_sub.execution.hooks import (
    BeforeModelHookInput, HookResult, Middleware)
from nexau.core.messages import Message, Role, TextBlock

# --USER-HOOK-START--
def before_model(hook_input):
    phase = hook_input.get("phase", 0)
    if phase == 0:
        return "Phase 0/4: Start with scan_rectangles() to find mackerel-rich regions. Sample 50-100 rectangles, keep top 10."
    elif phase == 1:
        return "Phase 1/4: Build L-shapes and stepped polygons from top rectangles. Exclude sardine clusters by cutting corners."
    elif phase == 2:
        return "Phase 2/4: Expand polygon toward coordinate boundaries (0 or 100000). Fish often cluster at corners."
    elif phase == 3:
        return "Phase 3/4: Refine best polygon with local edge perturbations (±1 to ±10). Hill climbing with restarts."
    elif phase == 4:
        return "Phase 4/4: Validate polygon (non-self-intersecting, axis-aligned, perimeter ≤ 400,000). Output best result."
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
