---
name: single-edit-search
description: Systematically vary ONE parameter in ONE pattern. Max 15 evals. Stop immediately if score > 1.0.
---

# Single Edit Search for Erdos Problem

## Core Principle
One parameter change, one evaluation, one decision.

## Pattern 13: Bipartite Threshold Search
Target lines:
  "latent = latent + jnp.where(x < a, 3.0, -3.0)"

Sequential edits (only ONE per evaluation):
  1. x < 0.3
  2. x < 0.25  
  3. x < 0.2
  4. x < 0.15

After each edit: CALL evaluate_solution immediately.
If score > 1.0: SUBMIT and finish.

## Pattern 12: Golomb Mark Spacing
Target: "marks = jnp.array([0.0, 0.4, 0.8, 1.2, 1.6])"

Sequential edits:
  1. [0.0, 0.35, 0.7, 1.05, 1.4]
  2. [0.0, 0.3, 0.6, 0.9, 1.2]
  3. [0.0, 0.45, 0.9, 1.35, 1.8]

After each: EVALUATE. If score > 1.0: SUBMIT.

## Budget Discipline
- Maximum 15 evaluations TOTAL
- Do NOT reuse previous evaluations
- Do NOT try multiple patterns before evaluating
- Stop after 15 evals even without success (we need to conserve budget)

## Critical: The seed already has 15 patterns. We don't need new patterns,
we need BETTER versions of existing ones. Start with the simplest: bipartite.
