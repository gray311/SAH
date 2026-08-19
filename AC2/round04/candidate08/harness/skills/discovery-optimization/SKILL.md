---
name: discovery-optimization
description: "Maximize C2 using template-based mutation. Start with step-function templates (A-H). After each edit, probe or eval immediately. If score drops > 0.005, switch template. Target: combined_score > 1.026."
---

# C2 Optimization with Templates: Action-First Exploration

## Objective
Beat the current best C2 = 0.8963. Your harness needs to produce functions that achieve higher values.

## Core Principle: Templates Beat Abstract Planning

Don't spend iterations planning "let me explore 5 families." Instead:
1. Pick a template
2. Copy it, change ONE number
3. Evaluate
4. Repeat or switch

## Step-by-Step Protocol

### Phase 1: Baseline (1 eval)
- Call evaluate_solution once to confirm baseline (~1.025)
- Note what your current _create_initializer looks like

### Phase 2: Template Exploration (Your Main Work)
For each template A-H below:
1. Copy the template code
2. Modify ONE parameter (h, start, end, or heights)
3. Call edit_solution to replace your _create_initializer
4. Call probe_solution to quickly check direction
5. If probe_score looks promising (close to or above baseline), call evaluate_solution
6. Track: template, parameter change, probe score, eval score
7. If 2 consecutive probes drop score by > 0.005, switch to next template

### Phase 3: Convergence or Switch
- If a template yields combined_score > 1.026: deepen it (more variants, finer tuning)
- If no template beats baseline after trying all 8: call finish and let others try

## Template Reference (COPY THESE EXACT PATTERNS)

A. Narrow step (h=1.0, width 0.2-0.8): start=0.2n, end=0.8n
B. Wide step (h=1.1, width 0.15-0.7): start=0.15n, end=0.7n
C. Tall narrow (h=1.5): start=0.25n, end=0.75n
D. Multi-level 3: heights [1.0, 2.0, 1.2] at [0.1n-0.22n, 0.22n-0.5n, 0.5n-0.8n]
E. Multi-level 4: heights [0.8, 2.2, 1.0] at [0.1n-0.3n, 0.3n-0.6n, 0.6n-0.9n]
F. Gaussian-like: softplus(0.5*sin(...))
G. Triangular: h=2.0 (0.3n-0.7n), h=1.8 (0.35n-0.65n)
H. Asymmetric 4-level: heights [1.0, 2.5, 1.5, 0.8] at 4 regions

## Key Rules
- ONE parameter change per edit
- Probe before full eval (use 3 probes per template)
- Stop immediately if score drops > 0.005 (this template is wrong direction)
- Target: first template to reach > 1.026
