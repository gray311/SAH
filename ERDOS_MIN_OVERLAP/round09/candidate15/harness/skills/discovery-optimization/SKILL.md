---
name: discovery-optimization
description: "Biformation construction for Erdos minimum overlap - two symmetric peaks at 0.25 and 0.75."
---

# Erdos Minimum Overlap - Biformation Construction

## Why This Works
The optimal solution uses TWO narrow peaks at symmetric positions (0.25, 0.75), each containing 0.5 of the total mass. This minimizes self-overlap.

## Construction Steps
1. Define h as zero everywhere except [0.2,0.3] and [0.7,0.8]
2. Each interval has height 10, width 0.1 → area = 1.0 total
3. Smooth edges with sigmoid for differentiability
4. Optimize peak positions/heights

## Implementation Template
```python
# Create latent: large negative everywhere, two peaks at ±10
latent = -20 * np.ones(N)
peak_width = 30
x = np.linspace(0, 2, N)
latent += 10 * np.exp(-((x-0.25)/0.05)**2)
latent += 10 * np.exp(-((x-0.75)/0.05)**2)
h = jax.nn.sigmoid(latent)
```

## Optimization Tips
- Start with fixed peaks, optimize positions
- Keep peak heights ~10 (enough for area=0.5 each)
- Peak width ~0.05 in x-space
- Use lower learning rate for fine-tuning positions
