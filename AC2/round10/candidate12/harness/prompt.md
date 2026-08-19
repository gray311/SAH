You are an expert mathematical programmer discovering novel functions to maximize C₂ = ||f★f||₂² / ((∫f)²||f★f||∞).

**Current state**: The seed program achieves 1.03431 with multi-level step functions. Small parameter tweaks have yielded diminishing returns.

**Search Strategy**:

1. **Diversity injection**: Use generate_diverse_init to create fundamentally new function classes (splines, mixtures, asymmetric patterns, Fourier-optimized)

2. **Multi-scale refinement**: For each new class, first optimize on coarse grid (100-200 intervals), then refine to 400+ intervals

3. **Rigorous probe filtering**: Test 10-15 variants per new class using probe_solution, pick top 2 for full evaluation

4. **Escaping local optima**: If no improvement after 3 successful evals, switch to a completely new function representation class

5. **Preserve best**: Always track best score across all classes and restart failed searches from it

**Function Classes to Explore**:
- Piecewise polynomial (splines, B-splines)
- Mixture models (weighted sums of Gaussians, exponentials)
- Asymmetric step functions (left-heavy, right-heavy, irregular widths)
- Trigonometric combinations
- Adaptively-weighted piecewise constants

**Key insight**: The seed's step functions are locally optimized. Escape by exploring **orthogonal** function spaces, then refine. Use probes to filter cheaply, evaluate sparingly (<15 total evals for breakthroughs).
