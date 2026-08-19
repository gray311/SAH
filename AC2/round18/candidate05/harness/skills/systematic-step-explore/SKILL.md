---
name: systematic-step-explore
description: Exploit step-function architecture (seed=1.042). Use controlled, valid edits to explore parameter space.
---

# Systematic Step-Function Exploration

## Core Principle
Seed achieves 1.042 - step functions work. Systematically perturb parameters with VALID Python syntax. Don't abandon for untested families.

## Mutation Types
1. HEIGHT: h -> h*0.9 or h*1.1
2. POSITION: int(0.30*n) -> int(0.27*n) or int(0.33*n)
3. WIDTH: adjust interval size by +/-10%

## Execution
1. After eval, get best program
2. Call mutate_step_params to get 3 variants
3. Probe all, evaluate top 2
4. Best becomes new base

## Valid Syntax
- CORRECT: f.at[int(0.25*n):int(0.75*n)].set(1.40)
- WRONG: f.at[0.25*n:0.75*n].set(1.40)
- ALWAYS: f = jax.numpy.maximum(f, 0.001)

## Flow
- Phase 1 (1-12): structured variation
- Phase 2 (13-24): combinations
- Phase 3 (25-30): finetuning
- Reset to seed if stuck
