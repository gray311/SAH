---
name: hybrid-search-protocol
description: Strategy for efficient mutation exploration using structural analysis, targeted mutations, and hybrid ranking.
---

# Hybrid Search Protocol for C₂ Maximization

## Overview

Combine structural analysis, targeted mutations, and hybrid evaluation for efficient exploration.

## Phase 1: Structural Analysis

1. Call pattern_analyzer to get structural insights about the current pattern
2. Note key characteristics: symmetry, height variance, interval widths, pattern type
3. Identify specific improvement opportunities from the suggestions

## Phase 2: Targeted Mutation Generation

1. Call pattern_mutator with insights from analysis
2. Generate 2-3 mutations focused on the identified weaknesses
3. Prefer mutations that directly address the pattern's characteristics

## Phase 3: Hybrid Ranking

1. Run hybrid_evaluator on all generated mutations
2. Rank by estimated C₂ score
3. Select top 1-2 mutations for full evaluation

## Phase 4: Full Evaluation

1. Call evaluate_solution on the top-ranked mutation(s)
2. Record results and compare to baseline
3. If improvement: continue with this mutation type
4. If no improvement after 2-3 attempts: analyze again and try different mutation type

## Key Principles

- Don't skip structural analysis - it guides better mutations
- Always rank before evaluating - save your budget
- Combine analysis insights with mutation types for more focused search
- Track which pattern characteristics correlate with improvements
