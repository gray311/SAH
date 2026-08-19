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
    current_program = ctx.get_best_program() if ctx.get_best_program() else ctx.get_program()
    if not current_program:
        return {"error": "No program to analyze"}
    
    try:
        f_values = [float(x) for x in current_program.strip().split('\n') if x.strip()]
        if len(f_values) < 100:
            return {"error": "Need ≥100 points"}
        
        f = np.array(f_values[:150])
        N = len(f)
        h = 1.0 / N
        
        # Compute baseline C₂
        f_nn = np.maximum(f, 0)
        padded = np.concatenate([f_nn, np.zeros(N)])
        fft_f = np.fft.fft(padded)
        conv = np.fft.ifft(fft_f * fft_f).real
        
        y_pts = np.concatenate([np.array([0.0]), conv, np.array([0.0])])
        y1, y2 = y_pts[:-1], y_pts[1:]
        l2_sq = np.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))
        norm1 = np.sum(np.abs(conv)) / (len(conv) + 1)
        norm_inf = np.max(np.abs(conv))
        c2 = l2_sq / (norm1 * norm_inf)
        
        # Simple sensitivity: test 3 variants
        variants = []
        
        # Variant 1: Increase peak height by 10%
        peak_idx = np.argmax(conv)
        f_var1 = f.copy()
        f_var1[peak_idx] += 0.1 * f[peak_idx]
        f_var1_nn = np.maximum(f_var1, 0)
        padded1 = np.concatenate([f_var1_nn, np.zeros(N)])
        fft1 = np.fft.fft(padded1)
        conv1 = np.fft.ifft(fft1 * fft1).real
        y1_pts = np.concatenate([np.array([0.0]), conv1, np.array([0.0])])
        y1_1, y1_2 = y1_pts[:-1], y1_pts[1:]
        l2_sq1 = np.sum((h / 3) * (y1_1**2 + y1_1 * y1_2 + y1_2**2))
        norm1_1 = np.sum(np.abs(conv1)) / (len(conv1) + 1)
        norm_inf1 = np.max(np.abs(conv1))
        c2_1 = l2_sq1 / (norm1_1 * norm_inf1)
        variants.append({"variant": "increase_peak_10pct", "c2": float(c2_1)})
        
        # Variant 2: Widen the peak
        start = int(N * 0.25)
        end = int(N * 0.75)
        f_var2 = f.copy()
        f_var2[start:end] += 0.05
        f_var2_nn = np.maximum(f_var2, 0)
        padded2 = np.concatenate([f_var2_nn, np.zeros(N)])
        fft2 = np.fft.fft(padded2)
        conv2 = np.fft.ifft(fft2 * fft2).real
        y2_pts = np.concatenate([np.array([0.0]), conv2, np.array([0.0])])
        y2_1, y2_2 = y2_pts[:-1], y2_pts[1:]
        l2_sq2 = np.sum((h / 3) * (y2_1**2 + y2_1 * y2_2 + y2_2**2))
        norm1_2 = np.sum(np.abs(conv2)) / (len(conv2) + 1)
        norm_inf2 = np.max(np.abs(conv2))
        c2_2 = l2_sq2 / (norm1_2 * norm_inf2)
        variants.append({"variant": "widen_peak_5pct", "c2": float(c2_2)})
        
        # Variant 3: Add side lobes
        f_var3 = f.copy()
        f_var3[int(N*0.1):int(N*0.2)] = 0.3
        f_var3[int(N*0.8):int(N*0.9)] = 0.3
        f_var3_nn = np.maximum(f_var3, 0)
        padded3 = np.concatenate([f_var3_nn, np.zeros(N)])
        fft3 = np.fft.fft(padded3)
        conv3 = np.fft.ifft(fft3 * fft3).real
        y3_pts = np.concatenate([np.array([0.0]), conv3, np.array([0.0])])
        y3_1, y3_2 = y3_pts[:-1], y3_pts[1:]
        l2_sq3 = np.sum((h / 3) * (y3_1**2 + y3_1 * y3_2 + y3_2**2))
        norm1_3 = np.sum(np.abs(conv3)) / (len(conv3) + 1)
        norm_inf3 = np.max(np.abs(conv3))
        c2_3 = l2_sq3 / (norm1_3 * norm_inf3)
        variants.append({"variant": "add_side_lobes", "c2": float(c2_3)})
        
        return {
            "baseline_C2": float(c2),
            "combined_baseline": float(c2 / 0.8962799441554086),
            "sensitivity_variants": sorted(variants, key=lambda x: -x["c2"])[:3],
            "recommendation": "Try the top variant from sensitivity_variants"
        }
    except Exception as e:
        return {"error": str(e)}