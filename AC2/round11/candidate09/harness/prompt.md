You are optimizing C₂ = ||f★f||₂² / ((∫f)²||f★f||∞) for the second autocorrelation inequality.

CURRENT BEST: 1.03663 (step function patterns)
TARGET: Beat this to establish a new record

CRITICAL STRATEGY: Do NOT try to invent entirely new pattern architectures. The seed program's 13 multi-level step patterns are already sophisticated. Your job is LOCAL OPTIMIZATION within these pattern families.

METHOD:
1. START: Call param_tuner to analyze the current best pattern and generate 3-5 concrete parameter variations (height adjustments: ±0.02-0.10, width shifts: ±2-5% of interval)

2. ITERATION: For each variation:
   - Call param_tuner ONCE to generate variations
   - Call evaluate_solution ONCE per variant
   - Keep track of which variant improved
   - IF improved: generate MORE variations from that improved variant (not the original!)
   - IF no improvement: generate variations from a DIFFERENT seed pattern

3. EXPLOITATION: When you find an improvement:
   - Immediately generate 2-3 refinements of THAT variant
   - Do NOT restart with new random patterns
   - Drill down until you hit a local optimum, THEN try a different seed

4. DIVERSITY: After exhausting one seed pattern's local optima (3-4 consecutive no-improvements), switch to a different seed pattern from the 13 options

FAILURE MODES:
- DO NOT spend 5+ evals on one pattern before finding any improvement
- DO NOT try "asymmetric" or "smooth transition" - these don't work with the step-pattern codebase
- DO NOT use probe_solution - it's unreliable; use evaluate_solution only
- DO explore BOTH height and width parameters, not just heights
