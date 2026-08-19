---
name: direct-construction-eval
description: Bypass slow training, directly construct and FFT-evaluate step function candidates. Use all 30 evals for this.
---

# Direct Construction + FFT Evaluation Strategy

## The Problem
The seed optimizer runs 59,000 training steps per evaluation. This is 100-1000x slower than necessary.

## The Solution
1. EDIT to remove the optimizer: Delete or comment out the training loop
2. DIRECT CONSTRUCTION: Create step functions analytically
3. FFT EVALUATION: Use _compute_c5_bound (the FFT function) to evaluate each candidate in ~10ms
4. SEARCH LOOP: Edit the main code to iterate over 50-100 candidates
5. BEST CANDIDATE: Pick the one with lowest c5_bound
6. SINGLE EVALUATION: Call evaluate_solution once on the best candidate

## Example Edit Structure
Instead of running 59000 training steps, do this:
- Create candidate constructions
- For each, compute FFT-based c5_bound in ~10ms
- Pick the best candidate
- Call evaluate_solution ONCE

## Why This Works
- FFT evaluation: 10ms per candidate
- 59000-step training: 30+ seconds per evaluation
- Result: Test 3000+ candidates per evaluation budget
- Even 10x worse than seed is possible with this approach
