---
name: incremental-pattern-expansion
description: Method for incrementally expanding step patterns. Start with existing patterns, add levels, create asymmetry, or narrow peaks. Use pattern_generator for code templates.
---

# Incremental Pattern Expansion for C₂ Maximization

## Core Principle

Don't redesign from scratch - start with existing patterns and make concrete modifications.

## Step 1: Analyze Current Pattern

- Extract heights: find max_height, min_height, average height
- Count levels: how many distinct height values?
- Identify symmetry: is the pattern symmetric?

## Step 2: Choose Expansion Strategy

**Strategy A: Add a Level**
- Take 4-level pattern → add 5th level at intermediate height
- Example: [0.6, 1.0, 1.5, 2.0] → [0.5, 0.8, 1.0, 1.4, 2.0]

**Strategy B: Create Asymmetry**
- Shift heights so left side ≠ right side
- Example: [0.5, 1.2, 0.8, 1.4] → [0.4, 1.3, 0.7, 1.5]

**Strategy C: Narrow Peak**
- Create a very tall, narrow central peak
- Example: [0.3, 2.5, 0.3] - tall middle, small wings

**Strategy D: Smooth Transition**
- Use gradual height changes (exponential-like)
- Example: [0.5, 0.7, 0.9, 1.0, 0.8] - smooth progression

## Step 3: Get Code Template

1. Call pattern_generator with pattern_type = your chosen strategy
2. Get the code_template it returns
3. This is ready-to-use code for _create_step_initializer

## Step 4: Edit and Evaluate

1. Use edit_solution to replace _create_step_initializer with the template
2. Call evaluate_solution ONCE
3. Record the score

## Step 5: Refine or Repeat

- If score > 1.03663: adjust heights by ±0.1, evaluate again
- If score ≤ 1.03663: call pattern_generator with different pattern_type

## Key Rules

- Use pattern_generator FIRST (don't write code from scratch)
- ONE evaluation per iteration
- Small changes only (heights ±0.1, positions ±5%)
- Keep trying until you find something > 1.03663
