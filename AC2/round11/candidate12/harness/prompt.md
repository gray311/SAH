You are optimizing C₂ = ||f★f||₂² / ((∫f)²||f★f||∞). The seed program has 13 multi-level step patterns achieving 1.03663.

CRITICAL: DO NOT try to invent entirely new pattern classes. Instead, use iterative hill-climbing on EXISTING patterns.

Strategy:
1. Pick ONE pattern from the 13 seed patterns (start with pattern 6 or 11, which have multiple levels)
2. Make a SMALL targeted mutation: adjust ONE height parameter by ±0.05-0.1, OR shift ONE boundary by ±2-3 intervals
3. Evaluate immediately. If improved, continue mutating the SAME pattern for 2-3 more iterations.
4. If no improvement after 3 iterations, pick a DIFFERENT pattern and repeat.
5. Never generate 5+ level patterns in one edit. Add complexity gradually.

Why this works: Small, incremental changes are more likely to improve C₂ than radical redesigns. The seed patterns are well-optimized; perturb them carefully.

Budget: 30 evals. Use 2-3 evals per pattern exploration, then switch patterns.

Pattern types to start with: pattern 6 (four-level), pattern 11 (pyramid), pattern 3 (multi-level asymmetric)
