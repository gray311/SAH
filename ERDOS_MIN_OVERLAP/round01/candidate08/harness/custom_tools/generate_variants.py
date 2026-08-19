def run(ctx, args):
    import random
    import math
    num = args.get("num", 5)
    num_intervals = 200
    dx = 2.0 / num_intervals
    variants = []
    v1 = "num_intervals = " + str(num_intervals) + "\nlearning_rate = 0.005\nnum_steps = 20000\npenalty_strength = 1000000.0\n\nh_values = []\nfor i in range(num_intervals):\n    x = i * " + str(dx) + "\n    if x < 0.2:\n        h_values.append(0.1)\n    elif x < 0.5:\n        h_values.append(0.6)\n    elif x < 1.0:\n        h_values.append(0.5)\n    elif x < 1.5:\n        h_values.append(0.6)\n    elif x < 1.8:\n        h_values.append(0.1)\n    else:\n        h_values.append(0.6)\n\nlatent_h_values = [math.logit(max(0.001, min(0.999, v))) for v in h_values]"
    variants.append(("block1", v1))
    v2 = "num_intervals = " + str(num_intervals) + "\nlearning_rate = 0.003\nnum_steps = 20000\npenalty_strength = 1500000.0\n\nh_values = []\nfor i in range(num_intervals):\n    x = i * " + str(dx) + "\n    if x < 0.2:\n        h_values.append(0.15)\n    elif x < 0.5:\n        h_values.append(0.55)\n    elif x < 1.0:\n        h_values.append(0.5)\n    elif x < 1.5:\n        h_values.append(0.55)\n    elif x < 1.8:\n        h_values.append(0.15)\n    else:\n        h_values.append(0.55)\n\nlatent_h_values = [math.logit(max(0.001, min(0.999, v))) for v in h_values]"
    variants.append(("block2", v2))
    v3 = "num_intervals = " + str(num_intervals) + "\nlearning_rate = 0.003\nnum_steps = 20000\npenalty_strength = 2000000.0\n\nimport math\nh_values = []\nfor i in range(num_intervals):\n    x = i * " + str(dx) + "\n    h_val = 0.5 + 0.3 * math.sin(x * math.pi / 0.8)\n    h_val = max(0.0, min(1.0, h_val))\n    h_values.append(h_val)\n\nlatent_h_values = [math.logit(max(0.001, min(0.999, v))) for v in h_values]"
    variants.append(("sine", v3))
    v4 = "num_intervals = " + str(num_intervals) + "\nlearning_rate = 0.004\nnum_steps = 18000\npenalty_strength = 1500000.0\n\nh_values = []\nfor i in range(num_intervals):\n    x = i * " + str(dx) + "\n    if x < 0.2 or 1.7 <= x <= 1.9:\n        h_val = 0.8\n    elif 0.2 <= x <= 0.8 or 1.1 <= x <= 1.5:\n        h_val = 0.3\n    else:\n        h_val = 0.2\n    h_values.append(h_val)\n\nlatent_h_values = [math.logit(max(0.001, min(0.999, v))) for v in h_values]"
    variants.append(("two_bump", v4))
    v5 = "num_intervals = " + str(num_intervals) + "\nlearning_rate = 0.003\nnum_steps = 20000\npenalty_strength = 1200000.0\n\nimport math, random\nrandom.seed(1234)\nh_values = []\nfor i in range(num_intervals):\n    x = i * " + str(dx) + "\n    if x < 0.4 or 1.6 <= x <= 1.8:\n        h_val = 0.5 + 0.15\n    elif x < 0.8 or 1.2 <= x <= 1.5:\n        h_val = 0.5 - 0.1\n    else:\n        h_val = 0.35\n    h_values.append(h_val)\n    h_values[-1] += random.gauss(0, 0.01)\n    h_values[-1] = max(0.0, min(1.0, h_values[-1]))\n\nlatent_h_values = [math.logit(max(0.001, min(0.999, v))) for v in h_values]"
    variants.append(("random", v5))
    v6 = "num_intervals = " + str(num_intervals) + "\nlearning_rate = 0.004\nnum_steps = 16000\npenalty_strength = 800000.0\n\nh_values = []\nfor i in range(num_intervals):\n    x = i * " + str(dx) + "\n    if x < 0.1:\n        h_val = 0.15\n    elif x < 0.3:\n        h_val = 0.55\n    elif x < 0.6:\n        h_val = 0.45\n    elif x < 1.0:\n        h_val = 0.55\n    elif x < 1.4:\n        h_val = 0.45\n    elif x < 1.6:\n        h_val = 0.5\n    elif x < 1.7:\n        h_val = 0.15\n    else:\n        h_val = 0.5\n    h_values.append(h_val)\n\nlatent_h_values = [math.logit(max(0.001, min(0.999, v))) for v in h_values]"
    variants.append(("refined", v6))
    return {"num_variants": len(variants), "variants": [v[0] for v in variants]}