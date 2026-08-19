def run(ctx, args):
    import math
    import re
    import json
    import itertools
    import functools
    import collections
    import heapq
    import bisect
    import random
    import statistics
    import string
    import typing
    import dataclasses
    import numpy as np
    import pandas as pd
    
    num_intervals = args.get('num_intervals', 800)
    pattern_type = args.get('pattern_type', 'symmetric')
    concentration_center = args.get('concentration_center', 1.0)
    symmetry_axis = args.get('symmetry_axis', 1.0)
    
    N = num_intervals
    x = np.linspace(0, 2, N)
    domain_width = 2.0
    
    if pattern_type == 'symmetric':
        # Construct symmetric step function around symmetry_axis
        # Start with a basic symmetric pattern and add noise
        rng = np.random.default_rng(42)
        base = np.zeros(N)
        
        # Create multiple symmetric step patterns and blend
        for _ in range(5):
            step_width = rng.uniform(0.2, 0.8, N)
            symmetry_val = np.sin(2 * np.pi * np.abs(x - symmetry_axis) / 1.0)
            base = base + symmetry_val * step_width
        
        latent = np.tanh(base * 1.5)
        
    elif pattern_type == 'concentrated':
        # Concentrate mass around concentration_center
        rng = np.random.default_rng(43)
        latent = np.zeros(N)
        
        # Create Gaussian-like concentration
        width = rng.uniform(0.15, 0.3)
        dist = np.abs(x - concentration_center) / 1.0
        latent = np.exp(-dist / width) * np.tanh(3.0)
        
        # Add small symmetric perturbation
        perturbation = np.sin(4 * np.pi * (x - 1.0)) * 0.5
        latent = latent + perturbation * 0.3
        
    elif pattern_type == 'multi_scale':
        # Combine multiple scale patterns
        rng = np.random.default_rng(44)
        latent = np.zeros(N)
        
        # Fine scale: high-frequency oscillations
        latent += np.sin(10 * np.pi * x) * 0.5
        latent += np.sin(20 * np.pi * x) * 0.3
        
        # Coarse scale: broad shape
        latent += np.sin(2 * np.pi * x) * 1.5
        latent += np.cos(2 * np.pi * x) * 0.5
        
        # Add asymmetric bias
        latent += 2.0 * (x - 1.0)
        
    elif pattern_type == 'boundary':
        # Concentrate near boundaries (x=0 or x=2)
        rng = np.random.default_rng(45)
        latent = np.zeros(N)
        
        # Dual boundary concentration
        boundary_dist = np.minimum(x, 2.0 - x) / 1.0
        latent = np.exp(-boundary_dist / 0.3) * np.tanh(3.0)
        
        # Subtract middle to ensure integral constraint
        middle_penalty = np.exp(-np.abs(x - 1.0) / 0.5) * 0.5
        latent = latent - middle_penalty * 0.3
        
    else:  # random
        rng = np.random.default_rng(46)
        latent = rng.normal(0, 1.0, N)
        
    # Apply sigmoid to get h in (0, 1)
    h = 1 / (1 + np.exp(-latent))
    
    # Add constraint to ensure integral ≈ 1
    current_integral = np.sum(h) * (2.0 / N)
    if current_integral < 0.95 or current_integral > 1.05:
        scale = 1.0 / np.clip(current_integral, 0.01, 10.0)
        latent = latent + np.log(scale)  # Adjust sigmoid scale
        h = 1 / (1 + np.exp(-latent))
    
    # Return latent (h can be recomputed if needed)
    return {"latent": latent.tolist(), "h_mean": float(np.mean(h)),
            "h_integral": float(current_integral), "pattern": pattern_type}