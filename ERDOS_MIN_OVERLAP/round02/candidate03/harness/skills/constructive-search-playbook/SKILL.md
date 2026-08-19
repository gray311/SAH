---
name: constructive-search-playbook
description: Playbook for constructive search. Use systematic pattern exploration instead of gradient descent.
---

# Constructive Search Strategy
Always build candidates systematically. Never use gradient descent.

## Step 1: Grid Uniform Search
For N in [100, 200, 500, 1000, 2000]:
    Test even spacing, clustered, and alternating patterns
    Use probe_solution to rank 5-10 variants
    
## Step 2: Periodic Alternating
For period in [1, 2, 4, 8, 16, 32]:
    Try power values [1, 2, 4]
    Normalize to integral=1
    
## Step 3: Multi-step Construction
For steps in [3, 4, 5, 6]:
    Use positions from [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
    Heights: [0.1, 0.2, 0.3, 0.35, 0.4, 0.5]
    
## Step 4: Bimodal Ratios
For ratio in [0.25, 0.30, 0.333, 0.35, 0.375, 0.40]:
    For left_pos in [0.1, 0.2, 0.3, 0.4, 0.5]:
        For right_pos in [0.6, 0.7, 0.8, 0.9, 1.0]:
            Build candidate and normalize
    
## Step 5: Refine and Enemble
When a variant beats seed:
    Vary parameters by ±0.05
    Try ensembling with other good candidates
    Use analyze_spectrum_properties to guide search

## Success
Beat seed 0.999641, target combined_score > 1.0
