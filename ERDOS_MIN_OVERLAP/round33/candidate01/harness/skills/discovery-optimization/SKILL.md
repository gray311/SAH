---
name: discovery-optimization
description: "Analysis-driven mutation: (1) Find problematic k via correlation_analyzer, (2) Use mutation_generator to generate real edits targeting those k, (3) Probe before full evaluation."
---

# Erdos C5 - Real Mutation Strategy
## Phase 1: Analyze Correlation 1. CALL correlation_analyzer on current best 2. Note the top 5 problematic k values with highest overlap
## Phase 2: Generate REAL Mutations (CRITICAL) 1. CALL mutation_generator with target_shifts=[problematic_k values] - Use mutation_type: "narrow_peak", "shift_local", "flatten_region" - The tool will return ACTUAL edit commands (not just notes!) 2. Use the returned edits to modify h values
## Phase 3: Screen with Probe 1. Call probe_solution on each mutation candidate 2. Keep candidates with c5_bound < 0.375
## Phase 4: Evaluate and Iterate 1. Call evaluate_solution on best 1-2 candidates 2. If combined_score > 1.0, finish! 3. Otherwise, REPEAT from Phase 1 with new analysis
## Mutation Types: - narrow_peak: Make h peaks narrower (reduces overlap at small k) - shift_local: Shift h locally (can break overlap patterns) - flatten_region: Flatten h over problematic k window
## Rules: - ALWAYS start with correlation_analyzer - ALWAYS call mutation_generator to get real edits - NEVER edit randomly without analysis - Use probe before evaluate - Preserve integral(h)=1 (mutation tool handles this)
