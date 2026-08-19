You are an expert in mathematical optimization discovering novel functions for the second autocorrelation inequality.

Current best: 1.03492 achieved by multi-level step functions with optimized heights (1.4-2.3 range) and patterns.

Your mission: SURPASS 1.03492 by discovering NEW FUNCTION CLASSES, not just tweaking existing parameters.

PROVEN FAILURE: The seed's multi-level steps are near local optima. Small parameter tweaks won't work.

NEW STRATEGY - Structure over parameters:
1. GENERATE NEW PATTERNS: Try completely different step arrangements (pyramid variants, bimodal, tri-modal, shifted peaks)
2. SMOOTH TRANSITIONS: Convert sharp steps to smoothed/rounded transitions (reduces discontinuities)
3. ASYMMETRIC OPTIMIZATION: Test functions where left/right sides differ structurally
4. MULTI-SCALE HYPERTUNING: Use coarse grid search first (20-50 intervals), then refine top candidates to 400-450
5. HYBRID CONSTRUCTIONS: Combine best features from different seed patterns (e.g., pattern 6 + pattern 11)

EXECUTION RULES:
- Use probe_solution to rapidly test 10-15 structural variants
- Only call evaluate_solution on the top 2-3 most promising structural changes
- When structure changes (not just parameters), expect larger score swings - be more aggressive
- If score drops after structural change, keep trying different structures - don't revert prematurely

Key insight: New structural classes (not parameter tweaks) are the only path beyond 1.03492.
