---
name: discovery-optimization
description: "Generate valid step-function candidates using step_function_generator, then refine interval\nheights to minimize C5 bound. Use probe to screen integral constraint before full eval."
---

# Erdos Minimum Overlap - Step Function Search

## Core Strategy: True Step Functions, Not Smooth Sigmoids

The seed program fails because it optimizes smooth latent -> sigmoid, which cannot
discover sharp step functions efficiently. You MUST:

### Step 1: Generate Step Function with step_function_generator
- This creates N intervals where k have height H_high, 1 has height H_low
- H_high and H_low automatically satisfy integral(h)=1
- This is a VALID step function representation

### Step 2: Structure of the Search
For k intervals at H_high and 1 at H_low:
- H_high = (1 - H_low*(1-k)) / k
- Try different k values: 100, 200, 500, 1000 (fewer steps = simpler, may find global optimum)
- Try H_low = 0 (cleanest) or small values like 0.01, 0.05
- The optimizer then tweaks EXACTLY which intervals are high vs low (by editing the EVOLVE-BLOCK)

### Step 3: Use probe_solution aggressively
- After any edit, call probe_solution FIRST to check constraint
- Only proceed if integral(h) approx 1 (within tolerance)
- Use probes to rank many (k, H_low) combinations before full eval

### Step 4: Evaluation Strategy
- Call evaluate_solution only on candidates that:
  1. Pass probe screening (integral approx 1)
  2. Have reasonable H_high in [0,1] range
- Document which (k, H_low) combination worked best

## Why This Works
- Step functions are exactly what the problem asks for
- The FFT-based evaluator works perfectly on step functions
- With true step representation, the optimizer can find solutions the smooth latent cannot
