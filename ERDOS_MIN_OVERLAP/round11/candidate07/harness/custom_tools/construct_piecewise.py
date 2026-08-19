def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    rng = np.random.default_rng(123)
    constructions = {}
    x = np.linspace(0, domain, N)
    constructions['one_interval_0_1'] = ((x >= 0) & (x < 1)).astype(float)
    constructions['one_interval_05_15'] = ((x >= 0.5) & (x < 1.5)).astype(float)
    constructions['two_intervals_narrow'] = (((x >= 0.1) & (x < 0.4)) | ((x >= 1.3) & (x < 1.6))).astype(float)
    constructions['three_intervals_thirds'] = (((x >= 0) & (x < 1/3)) | ((x >= 1/3) & (x < 2/3)) | ((x >= 2/3) & (x < 1))).astype(float)
    constructions['asymmetric_two'] = (((x >= 0) & (x < 0.3)) | ((x >= 0.7) & (x < 1.3))).astype(float)
    return {"constructions": constructions}