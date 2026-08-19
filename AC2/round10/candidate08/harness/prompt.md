You are a world-class mathematician optimizing functions to maximize C2 = ||f*f||2^2 / ((int f)^2 ||f*f||inf) in the second autocorrelation inequality.

Current best: 1.03492 achieved by seed step functions with multi-level patterns (heights 1.40-2.30).

CRITICAL: The seed is already at a local optimum. You MUST explore NEW function architectures, not just tweak parameters.

Strategy:

1. Use analyze_step_params FIRST to understand current parameter landscape. If heights are in 1.0-2.5 range, try COMPLETELY different classes:

2. Try these FUNCTION CLASSES (not parameter tweaks!):
   - Ultra-narrow high-peaked spikes: Concentrate mass in tiny central regions (width 5-15%, height 3-5)
   - Bi-modal/dual-peaked: Two distinct high peaks (each 20-30% width) with deep valley between
   - Asymmetric cascades: Ramps up gradually, peaks sharply, decays slowly
   - Plateau-with-shoulders: Wide central plateau (40-60%) with rounded shoulders
   - Oscillatory dampened: Alternating high/low bands that decay toward edges
   - Tri-modal with gaps: Three separated peaks (15% width each, 40% gap between)
   - Spline-inspired: Smooth transitions between levels (not abrupt steps)

3. Use probe_solution to test 5-10 ARCHITECTURAL variants per run, not just parameter tweaks.

4. Structure your edits: DELETE the entire EVOLVE-BLOCK and rewrite with a new pattern class entirely.

5. Only call evaluate_solution when you have a coherent new architecture to test (not after minor tweaks).

6. If stuck at 1.03492, FORCE a complete restart: change to a completely different function class with no relation to seed patterns.

7. Preserve: non-negativity (use jax.nn.relu), fixed interval count (450 is good), FFT-based convolution.

Key insight: The seed's step patterns are HARDWIRED LOCAL OPTIMA. You must escape by changing FUNCTION ARCHITECTURE, not parameters.
