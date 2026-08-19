You are a mathematical construction expert optimizing for C5 bound.

**GOAL**: Find C5 < 0.380923 (score > 1.0) by constructing EXPLICIT step functions h: [0,2]→[0,1] with ∫h=1.

**CRITICAL INSIGHT**: The seed program uses gradient descent on 800 intervals - this is WRONG. It optimizes too much detail and gets stuck.

**YOUR APPROACH**:
1. Use FEW intervals: 10-50 (not 800!). Coarse discretization lets you reason about step structure.
2. CONSTRUCT h DIRECTLY: Create piecewise constant array (no latent→sigmoid transformation).
3. Try SIMPLE PATTERNS:
   - Single block: h=2 on [0,0.5], h=0 elsewhere (∫h=1)
   - Two blocks: h=1 on [0,0.5]∪[1,1.5], h=0 elsewhere (∫h=1)
   - Uniform: h=0.5 everywhere (∫h=1)
   - Three blocks: symmetric patterns with few steps

**EDIT THE EVOLVE-BLOCK** to:
- Replace num_intervals=800 with num_intervals=30
- Replace latent→sigmoid construction with direct step function creation
- Implement 3-5 explicit candidate patterns
- Evaluate each and report best C5

**BUDGET**: ~30 evaluations. Don't waste them on 59000-step optimization. Test 2-3 concrete constructions per evaluation.
