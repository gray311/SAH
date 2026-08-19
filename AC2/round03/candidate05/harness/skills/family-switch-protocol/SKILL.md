---
name: family-switch-protocol
description: Protocol for switching function families in C2 optimization. Uses code_snippet_generator for templates. Strict 2-eval limit per family. Switch on stagnation.
---

# C2 Family Switch Protocol

## Core Principle
STOP tuning piecewise-linear. SWITCH to new families using code_snippet_generator.

## Protocol

### Step 1: Generate Templates
Call code_snippet_generator with family="steps" or family="gaussian".

### Step 2: Insert Template
Copy first template. Delete old _create_initializer. Paste new one.

### Step 3: Create Variants
Use variant_parameter_tweaker for 3-5 parameter variants.

### Step 4: Probe All
Call probe_solution on each variant. Rank them.

### Step 5: Evaluate Top 2
Pick 2 highest. Call evaluate_solution.

### Step 6: Decision
Improvement? Deepen. No improvement? SWITCH families.

## Rules
- 5+ probes per family
- Max 2 evals per family
- Switch on stagnation
- Use code_snippet_generator before editing

## Tools
| Tool | Purpose |
|------|--------|
| code_snippet_generator | Generate templates |
| variant_parameter_tweaker | Create variants |
| probe_solution | Rank variants |
| evaluate_solution | Confirm top 2 |

## Expected Flow
1. Generate templates
2. Insert and tweak
3. Probe variants
4. Evaluate top 2
5. Switch if no improvement
