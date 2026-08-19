---
name: discovery-optimization
description: "Generate diverse patterns, pick best, convert to code edit, evaluate. Focus on pattern diversity (Golomb, bipartite, triangular) with exact integral constraint. Always use best_pattern_to_code to translate patterns to edits."
---

# Erdos C5 Optimization Strategy
## Phase 1: Pattern Generation and Code Conversion
1. CALL search_patterns(temperature=0.5) - Generates 5 diverse initial step functions with precomputed c5_bound - Patterns: Golomb (4 marks), Bipartite (threshold), Triangular (single peak), Multi-peak, Laplace
2. IDENTIFY the best pattern: - Find candidate with lowest c5_bound - Must have c5_bound < 0.375 to warrant full evaluation
3. CALL best_pattern_to_code(pattern_type=<best_pattern_type>) - This generates the EXACT code edit to use this pattern in the EVOLVE-BLOCK - The edit replaces the random initialization with the deterministic pattern
4. APPLY the edit using edit_solution - The edit_solution tool applies the diff to the seed program
5. CALL evaluate_solution - Run the full 59000-step optimization with the new initialization - Check combined_score
## Phase 2: Iteration
If combined_score <= 1.0: - Try the next best pattern from search_patterns - Or call search_patterns(temperature=0.8) for different patterns - Only after exhausting patterns, tune hyperparameters
## Key Rules
- ALWAYS use best_pattern_to_code to convert patterns to code edits - NEVER evaluate raw patterns without applying the edit first - Focus on patterns with c5_bound < 0.375 - Track the pattern_type that gave best c5_bound
