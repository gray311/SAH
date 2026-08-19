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
    
    n_patterns = args.get('n_patterns', 5)
    base_idx = args.get('base_pattern_idx', 0)
    n = 400
    
    patterns = {
        0: {'h': 1.42, 's': 0.25, 'e': 0.75},
        1: {'h': 1.52, 's': 0.28, 'e': 0.72},
        2: {'h': 1.62, 's': 0.30, 'e': 0.70},
        3: {'h': [0.92, 1.92, 0.92], 's': [0.15, 0.25, 0.75], 'e': [0.25, 0.75, 0.85]},
        4: {'h': [1.12, 2.32, 1.42], 's': [0.1, 0.2, 0.5], 'e': [0.2, 0.5, 0.7]},
        5: {'h': 1.52, 's': [0.2, 0.5], 'e': [0.4, 0.8]},
        6: {'h': [0.72, 1.32, 1.72, 1.02], 's': [0.05, 0.2, 0.35, 0.65], 'e': [0.2, 0.35, 0.65, 0.95]},
        7: {'h': [0.82, 2.02, 0.82], 's': [0.1, 0.3, 0.7], 'e': [0.3, 0.7, 0.9]},
        8: {'h': [0.62, 1.02, 1.52, 1.22], 's': [0.05, 0.25, 0.45, 0.65], 'e': [0.25, 0.45, 0.65, 0.95]},
        9: {'h': 1.72, 's': 0.22, 'e': 0.78},
        10: {'h': 1.66, 's': 0.24, 'e': 0.76},
        11: {'h': [0.72, 1.52, 2.12, 1.52, 0.72], 's': [0.05, 0.2, 0.4, 0.6, 0.8], 'e': [0.2, 0.4, 0.6, 0.8, 0.95]},
        12: {'h': [0.62, 1.32, 2.02, 1.32, 0.62], 's': [0.03, 0.18, 0.38, 0.62], 'e': [0.18, 0.38, 0.62, 0.95]},
    }
    
    height_mods = [0.90, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35]
    pos_shifts = [-0.02, -0.01, 0.0, 0.01, 0.02]
    
    base = patterns[base_idx]
    variations = []
    i = 0
    
    while len(variations) < n_patterns:
        f = np.zeros(n)
        
        if isinstance(base['h'], list):
            h_list = base['h']
            s_list = base['s']
            e_list = base['e']
            
            for h_mod in height_mods:
                h_new = [round(h * h_mod, 2) for h in h_list]
                for p_mod in pos_shifts:
                    s_new = [max(0, min(1, s + p_mod)) for s in s_list]
                    e_new = [max(0, min(1, e + p_mod)) for e in e_list]
                    if all(s < e for s, e in zip(s_new, e_new)):
                        start_idx = int(s_new[0]*n)
                        end_idx = int(e_new[0]*n)
                        f[start_idx:end_idx] = h_new[0]
                        for j in range(1, len(e_new)):
                            start_idx = int(s_new[j]*n)
                            end_idx = int(e_new[j]*n)
                            f[start_idx:end_idx] = h_new[j]
                        variations.append({'index': i, 'f': f, 'pattern_id': base_idx, 'h': h_new, 's': s_new, 'e': e_new})
                        break
                if len(variations) >= n_patterns:
                    break
            if len(variations) >= n_patterns:
                break
        else:
            for h_mod in height_mods:
                h_new = round(base['h'] * h_mod, 2)
                for p_mod in pos_shifts:
                    s_new = max(0.05, min(0.95, base['s'] + p_mod))
                    e_new = max(0.05, min(0.95, base['e'] + p_mod))
                    if s_new < e_new:
                        start_idx = int(s_new*n)
                        end_idx = int(e_new*n)
                        f[start_idx:end_idx] = h_new
                        variations.append({'index': i, 'f': f, 'pattern_id': base_idx, 'h': h_new, 's': s_new, 'e': e_new})
                        break
                if len(variations) >= n_patterns:
                    break
            if len(variations) >= n_patterns:
                break
        
        i += 1
    
    return variations