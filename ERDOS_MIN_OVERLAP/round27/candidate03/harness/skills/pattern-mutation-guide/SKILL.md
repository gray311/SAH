---
name: pattern-mutation-guide
description: Use pattern_mutation_generator to create integral-normalized candidates. Filter c5_bound < 0.375, then train with num_restarts=1, num_steps=30000.
---

# Pattern Mutation Guide

1. CALL pattern_mutation_generator() to get 4 integral-normalized variants
2. FILTER: keep only candidates with integral ~ 1.0 (skip others), c5_bound < 0.375
3. For each kept candidate, train with num_restarts=1, num_steps=30000
4. USE probe to check c5_bound after training
5. FULL EVAL if combined_score > 0.9995
