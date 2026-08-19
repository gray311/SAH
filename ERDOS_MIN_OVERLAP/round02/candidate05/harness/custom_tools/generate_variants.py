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

    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(42)

    def sigmoid(z):
        return 1.0 / (1.0 + np.exp(-z))

    def create_bimodal(pos, width=0.3):
        x = np.linspace(0, domain, N)
        h = sigmoid(-5.0 * (x - pos) / width + 3.0)
        integral = np.sum(h) * dx
        h = h / integral
        return h

    def create_uniform():
        h = rng.uniform(0.3, 0.7, (N,))
        integral = np.sum(h) * dx
        h = h / integral
        return h

    def create_alternating():
        x = np.linspace(0, domain, N)
        h = (np.sin(2 * np.pi * x) + 2.0) / 3.0
        integral = np.sum(h) * dx
        h = h / integral
        return h

    def create_shifted(offset):
        x = np.linspace(0, domain, N)
        h = sigmoid(-6.0 * (x - offset) / 0.5 + 4.0)
        integral = np.sum(h) * dx
        h = h / integral
        return h

    results = {}
    # Bimodal at different positions
    for pos in [0.2, 0.8]:
        h = create_bimodal(pos)
        results[f'bimodal_pos{pos:.1f}'] = h
    # Uniform
    h = create_uniform()
    results['uniform'] = h
    # Alternating
    h = create_alternating()
    results['alternating'] = h
    # Shifted
    for off in [0.3, 0.7]:
        h = create_shifted(off)
        results[f'shifted{off:.1f}'] = h

    # Small perturbations of best patterns
    rng = np.random.default_rng(42)
    best_keys = ['bimodal_pos0.2', 'shifted0.3', 'shifted0.7', 'uniform']
    for k in best_keys[:4]:
        h = results[k] + rng.normal(0, 0.1, (N,))
        integral = np.sum(h) * dx
        h = h / integral
        results[f'{k}_pert'] = h

    return {'variants': results}