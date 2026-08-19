---
name: discovery-optimization
description: "Structural search with adaptive resolution. Start with architecture diversity (interval count, height patterns), then refine based on spectral insights. Avoid over-parameterized 600-interval representations."
---

# C2 Maximizer: Structural Search Protocol
## Core Principle
The seed's 600-interval step functions are over-parameterized. Effective changes are STRUCTURAL (interval count, height distribution), not microscopic. DIVERSIFY architecture first.
## Phase 1: Architecture Diversification (iterations 1-10)
Step 1: Analyze Current Structure - Call analyze_function_structure to extract: interval count, unique height values, peak positions, symmetry
Step 2: Generate Architectural Variants Generate EXACTLY 4-5 variants, each with a DIFFERENT structural pattern:
Variant A (Downsample): - Reduce to 200-250 intervals - Maintain relative peak positions - Keep height distribution similar
Variant B (Upsample): - Increase to 800-1000 intervals - Smooth the signal by interpolating between current steps - Test if finer resolution helps
Variant C (Multi-Level): - Create 4-5 height levels instead of 2-3 - Distribute heights asymmetrically (e.g., 0.8, 1.4, 2.0, 1.0) - Test if complexity helps
Variant D (Narrow Peak): - Reduce support to 30% of domain - Increase peak height to 2.0-2.5 - Test if concentration helps
Variant E (Symmetric Break): - Break symmetry: left peak height != right peak height - Test 0.7-0.8 on left, 1.0-1.2 on right
Step 3: Probe and Evaluate - Call probe_solution on ALL 4-5 variants - Rank by probe score - Call evaluate_solution on TOP 1 only - If probe score < 1.0: skip full eval, try next architectural pattern
## Phase 2: Spectral Refinement (iterations 11-20)
Step 1: Analyze Function Structure - Call analyze_function_structure again - Note dominant frequency, smoothness, asymmetry
Step 2: Spectrally-Guided Variants Generate 3 variants:
Variant 1 (High-Frequency Boost): - Add rapid oscillations within intervals - Use JAX to create fine-scale variations
Variant 2 (Low-Frequency Smoothing): - Increase interval count to 1200+ - Smooth by low-pass filtering
Variant 3 (Mass Redistribution): - Shift mass from center to edges or vice versa - Test both directions
Step 3: Probe and Evaluate - Probe both, evaluate best - If gradient-like improvement stalls: switch to Phase 3
## Phase 3: Extreme Diversification (iterations 21-30)
Step 1: Try Extreme Architectures - 150-interval coarse function - Asymmetric multi-level (3-4 peaks of varying heights) - Gaussian-like smooth function (continuous approximation)
Step 2: Final Evaluation - Probe 3, evaluate best - Submit if c2 > 0.8962799441554086
## Key Rules - DIVERSIFY architecture: don't stay in one parameter regime - Avoid 600-interval if it failed - try 200, 800, or 1200 - Use structural insights, not parameter tweaks - Probes are cheap: explore 4-5 variants before each full eval
