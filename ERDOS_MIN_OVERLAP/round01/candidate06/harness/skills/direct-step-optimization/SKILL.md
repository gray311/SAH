---
name: direct-step-optimization
description: Use direct optimization over step function heights instead of gradient descent. Try multiple initial configurations and bounded internal search to find low C5 values.
---

# Direct Step Function Optimization
#
# Core Idea:
# The Erdos C5 problem requires finding h: [0,2]->[0,1] with integral(h)=1 minimizing max overlap.
# Gradient descent with sigmoid smoothing often gets stuck in local minima. Instead, directly
# optimize the step heights.
#
# Method:
# 1. DIRECT PARAMETERIZATION: Work with h[i] directly in [0,1] for each interval
# 2. CONSTRAINT SATISFYING: After any modification, renormalize to ensure integral(h) = 1
# 3. MULTIPLE STRATEGIES:
#    - Coordinate descent: optimize one interval at a time
#    - Grid search: try discrete values per interval
#    - Pattern-based: alternating, decreasing, block patterns
#    - Random restarts: different seeds with bounded search
# 4. BOUNDED INTERNAL SEARCH: Within each evaluation, run 4-10 different strategies and pick the best result
#
# Implementation:
# - Use numpy arrays directly (no JAX transformation overhead)
# - Clamp values to [0,1] after each modification
# - Normalize by dividing by integral(h) to enforce constraint
# - Keep each evaluation under 10 seconds
# - Report the configuration with lowest c5_bound
#
# Warning:
# - Do not rely on gradient methods alone
# - The FFT-based correlation can have multiple local minima
# - Different initializations often yield significantly different results
