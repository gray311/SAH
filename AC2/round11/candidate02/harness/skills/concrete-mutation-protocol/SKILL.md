---
name: concrete-mutation-protocol
description: Systematic protocol for using c2_mutation_engine to get concrete numerical mutations and implement them.
---

# Concrete Mutation Protocol for C₂ Maximization


## Overview

The c2_mutation_engine tool will give you CONCRETE numerical proposals (actual height values like 1.47, 2.33, 0.89), not symbolic expressions.


## Step 1: Call c2_mutation_engine

Call c2_mutation_engine at the start to get 4-6 concrete mutation proposals. Each proposal includes:
- A name for the pattern class
- Concrete height values (actual numbers)
- A rationale explaining why it should work


## Step 2: Choose and Implement ONE Proposal

Select ONE proposal that looks most promising. Then:

1. Find all occurrences of .set(NUMBER) in the _create_step_initializer method
2. Replace the numbers with the concrete values from your chosen proposal
3. Ensure the pattern structure (interval percentages) makes sense
4. Use edit_solution to apply the changes


## Step 3: Evaluate

Call evaluate_solution ONCE to test the implemented mutation.


## Step 4: Iterate

- If successful: call c2_mutation_engine again, refine the winning direction
- If unsuccessful: try a different proposal, or explore a new pattern class

## Key Principle

WORK WITH CONCRETE NUMBERS. The c2_mutation_engine gives you actual values like [0.82, 1.97, 0.71], not expressions like [min_h*0.7, max_h*1.35]. Use the actual numbers directly in your edits.
