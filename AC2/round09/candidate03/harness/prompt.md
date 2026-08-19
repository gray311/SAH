You are optimizing Python code to maximize C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞) for a non-negative function f.
The seed program already discovered high-quality multi-level step functions with C₂ ≈ 1.034.
Your goal: IMPROVE on this starting point, not break it.

CRITICAL RULES:
1. The seed program's step-function templates are ALREADY OPTIMIZED (heights like 1.42, 1.52, 1.62, 1.92, 2.12).
   DO NOT randomly change these heights. Instead, EXPERIMENTALLY PERTURB THEM.
2. Before full evaluation, ALWAYS use probe_solution to cheaply rank your variants.
   With 30 probes available and expensive full evals (budget of 30), use probes to find promising directions.
3. Make TARGETED, SMALL CHANGES: vary one parameter at a time (one height value, one interval width).
   The seed program's structure is valuable - don't rewrite it wholesale.
4. If your edit degrades performance, the seed's best version is automatically preserved.
   Try a DIFFERENT parameter variation, not a refinement of the failed one.
5. Use SEARCH/REPLACE diffs that modify ONLY the numeric parameters in the step-function definitions.

Strategy: The space of step-function parameters (heights, positions, widths) is continuous.
Use systematic exploration: perturb heights by ±0.05, shift positions by ±2 intervals, etc.
After each probe, decide whether to commit to full eval or explore another variant.
Call finish when probes show diminishing returns or you've exhausted promising directions.
