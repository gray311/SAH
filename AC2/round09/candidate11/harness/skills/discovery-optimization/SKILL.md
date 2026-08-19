---
name: discovery-optimization
description: "Optimize step function patterns for the second autocorrelation inequality. Systematically explore heights and positions, refine promising variants. Budget: 30 evals."
---

# Step Function Discovery for C₂ Maximization

## Strategy

1. **Seed exploration**: Start with the seed's 13 patterns (0-12)
2. **Systematic variation**: For each pattern:
   - Vary heights by 5-20%: try h*0.90, h*0.95, h*1.0, h*1.05, h*1.1, h*1.15, h*1.2
   - Shift positions by 1-2%: try s-0.02, s-0.01, s, s+0.01, s+0.02
   - For multi-level: vary each level's height independently
3. **Pattern diversity**: Try different base patterns (0-12)
   - Pattern 0-2: Simple single steps
   - Pattern 3-4: Multi-level with high middle
   - Pattern 5-8: Asymmetric patterns
   - Pattern 9-10: Very high central peaks
   - Pattern 11-12: Pyramid shapes
4. **Evaluate and refine**: Score each variant. Keep best. Deepen search on promising patterns.
5. **Mathematical intuition**: 
   - C₂ = ||f★f||₂² / ((∫f)² ||f★f||_{∞})
   - High, narrow peaks increase L² while keeping L∞ moderate
   - Multiple levels create interference effects
   - Width ~30-40% of domain works well for current best

## Edits

- Use SEARCH/REPLACE diffs for parameter changes
- Modify heights in _create_step_initializer method
- Adjust interval positions (int(0.XX * n))

## When to finish

Call finish when exhausted or budget depleted. Report best C₂ achieved.
