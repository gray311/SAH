---
name: earthos-piecewise-constructions
description: Use for Erdos C5 - Implement SPECIFIC piecewise constant functions with exact integral=1. Not random patterns.
---

# Erdos C5: Piecewise Constant Constructions

## Core Principle
h:[0,2]->[0,1], integral from 0 to 2 of h(x) dx = 1. Common mistake: forgetting to normalize!

## Construction Recipes

### Recipe A: Single Interval of Length 1
h(x) = 1 if x in [a, a+1], else 0
- For a=0: h=1 on [0,1]
- For a=0.5: h=1 on [0.5, 1.5] - SYMMETRIC, try this first!
- Integral: 1*1 = 1 exactly

### Recipe B: Two Intervals of Length 0.5 Each
h(x) = 1 if x in [a, a+0.5] U [b, b+0.5], else 0
- If a=0, b=1.5: h=1 on [0,0.5]U[1.5,2], integral=0.5+0.5=1

### Recipe C: Uniform with Plateaus
h(x) = alpha on [a,b], beta on [c,d], 0 elsewhere
- Choose alpha,beta,a,b,c to satisfy: alpha*(b-a)+beta*(d-c)=1 and 0<=alpha,beta<=1

### Implementation Template
x = jnp.linspace(0, 2, N)
h = jnp.where((x >= a) & (x < b), alpha, 0.0)
h = jnp.where((x >= c) & (x <= d), beta, h)

## Testing Order
1. Try h=1 on [0.5, 1.5] (symmetric, length 1)
2. Try h=1 on [0, 0.5] U [1.5, 2] (two intervals, length 1)
3. Try h=1 on [0, 1], h=0 on [1, 2] (half the domain)

## Common Pitfalls
- Forgetting to clamp h to [0,1]
- Wrong integral calculation (always verify integral(h)=1)
- Using too many intervals (start with 50-200)
