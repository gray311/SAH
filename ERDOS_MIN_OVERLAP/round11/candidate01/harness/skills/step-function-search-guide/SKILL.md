---
name: step-function-search-guide
description: Guide for searching the Erdos step-function space - generate step functions with different (k, H_low) pairs, use probes to screen, evaluate promising ones.
---

# Step-Function Search for Erdos Problem

## Problem Recap
Find step function h: [0,2] -> [0,1] with integral(h)=1 that minimizes
max_k integral h(x)(1-h(x+k)) dx.

## Why Step Functions?
The seed optimizer uses smooth sigmoids, which cannot efficiently find
sharp step functions. Use step_function_generator to create VALID step functions.

## Search Strategy

### Step 1: Choose (k, H_low) Pair
- k: number of high intervals (try 100, 200, 500, 1000, N-1)
- H_low: low interval height (try 0, 0.01, 0.05, 0.1, or let generator use 0)
- H_high is computed: (1 - H_low*(N-k)) / k

### Step 2: Generate with step_function_generator
- Call with your chosen (k, H_low, N=800)
- Verify "valid": True and 0 <= H_high <= 1
- This gives you a DISCRETE step function representation

### Step 3: Refine with EVOLVE-BLOCK editing
- Edit to: swap which intervals are high vs low
- OR: add more structure (e.g., make 2 low intervals instead of 1)
- OR: change k to a different number of high intervals
- Each edit creates a NEW step function candidate

### Step 4: Probe Screen
- After any edit, call probe_solution
- Check: does integral(h) approx 1? (use H_low, H_high from the generator)
- Skip full eval if constraint violated

### Step 5: Full Evaluation
- Call evaluate_solution on candidates that pass probe
- Track best combined_score

### Success Pattern
- Best known: 0.380923... (combined_score = 0.999855)
- Your goal: combined_score > 1.0 (c5_bound < 0.380923)
- Try: k=N-1 (one low interval), H_low=0, then optimizer finds best location
