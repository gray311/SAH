---
name: discovery-optimization
description: "Coarse-to-fine optimization for Erdos problem: Start with coarse discretization and multiple optimizers to escape local minima, then refine. Proven strategy beats pure fine-grained SGD."
---

# Erdos Minimum Overlap - Coarse-to-Fine Strategy

## Why Coarse-to-Fine Works

The problem is about finding a STRUCTURAL PATTERN (how many steps, where are the plateaus),
not fine-tuning 800 parameters.

## Method

### Step 1: Coarse Exploration (n=20-50 intervals)
- Try 10-20 different seeds
- Use SGD with momentum or L-BFGS
- Run 5000-15000 steps per seed
- Use probe_solution to rank

### Step 2: Select Best Coarse Structure
- Take top 2-3 from coarse phase by probe score
- Keep their structural pattern

### Step 3: Refinement (n=200-400 intervals)
- Refine the winning structure
- Use smaller LR (0.001-0.01)
- 3000-10000 steps

### Step 4: Final Evaluation
- Evaluate on full 800-interval discretization

## Key Principles

- Structure over parameters: Find the right STEP COUNT first
- Short and diverse: Many short searches beat few long ones
- Multiple optimizers: SGD+momentum and L-BFGS explore differently

## Tool Usage

- generate_coarse_variants: Get diverse coarse patterns
- probe_solution: Use extensively in coarse phase to rank quickly
- evaluate_solution: Only for final candidates

## Implementation Notes

Always apply sigmoid to latent: h = sigmoid(latent)
Always normalize to satisfy integral(h) = 1.0
