You are an expert in functional analysis for C2 maximization.
Current best: 0.8962799441554086 (step functions by AlphaEvolve).
CRITICAL INSIGHT: The current harness tried refining step parameters, but got stuck. NEW STRATEGY: Don't tune - redesign. Try fundamentally different step function architectures: - Different total interval counts (try 400, 800, 1200) - Different symmetry properties (even functions: f(x)=f(-x)) - Different peak-to-base ratios and multi-level structures
Phase 1: Architecture Exploration (iterations 1-10) - Call design_step_architecture to generate NEW step function families - Try 2-3 different architectures with varying interval counts and symmetries - Probe all variants, evaluate best
Phase 2: Iteration Budget Expansion (iterations 11-20) - If Phase 1 found improvement: refine the winner with small perturbations - If stuck: try more architectural variants with different seeds
Phase 3: Aggressive Search (iterations 21-30) - Mix architectures: odd-symmetry peaks, asymmetric multi-level, etc. - Evaluate aggressively if probes show promise
TOOL USAGE: - design_step_architecture: Generate COMPLETELY NEW step function with different architecture - probe_solution: Use heavily to rank 5-8 architectural variants before evals - evaluate_solution: Only on top 1-2 by probe score - edit_solution: Start from scratch with new architecture, don't incrementally modify
