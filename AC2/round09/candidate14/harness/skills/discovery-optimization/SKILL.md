---
name: discovery-optimization
description: "Design discrete step function patterns for C\u2082 maximization. Each iteration creates a complete new pattern by varying heights, positions, and structure - not just fine-tuning. Use probes to rank variants before full evaluation."
---

# C₂ Maximization: Step Function Pattern Discovery

Objective: Find piecewise-constant functions f(x) ≥ 0 maximizing C₂ = ||f★f||₂² / ((∫f)² ||f★f||_{∞}).

Core principle: This is DISCRETE CONSTRUCTION, not continuous optimization. The seed's 1.03431 score comes from specific step patterns. Your edits must create NEW patterns, not tweak parameters.

Pattern exploration strategy:
1. Start with 3-7 distinct levels (too many levels cause timeout)
2. Each iteration changes MULTIPLE things: heights, widths, AND positions
3. Try different pattern architectures:
   - Single high peak with symmetric wings
   - Multi-peak with varying heights
   - Asymmetric staircase
   - Pyramid/symmetric pyramid
   - Harmonic combinations (2-3 overlapping peaks)

Evaluation workflow:
1. Design 3-5 complete patterns internally
2. Call probe_solution on each (cheap, uses separate budget of ~30)
3. Pick top 1-2 and call evaluate_solution (consume real budget)
4. If score improves, build on that pattern. If worse, try different architecture.

Failure recovery:
- If evaluate errors: pattern too complex → reduce to 2-3 levels
- If score drops: fundamental pattern change needed, not parameter tuning
- If plateaued after 3 evaluations: change pattern family entirely

CRITICAL: Do NOT make small incremental edits. Each edit must encode a complete new pattern design. Keep functions simple to avoid timeouts.
