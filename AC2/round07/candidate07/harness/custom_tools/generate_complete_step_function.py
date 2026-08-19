def run(ctx, args):
    import random
    config = args
    
    num_intervals = config.get("num_intervals", random.choice([3, 5, 7]))
    symmetric = config.get("symmetric", True)
    peak_height = config.get("peak_height", random.uniform(1.2, 1.8))
    base_height = config.get("base_height", random.uniform(0.5, 0.9))
    
    intervals = []
    heights = []
    
    if symmetric:
        if num_intervals == 3:
            intervals = [(-0.5, -0.2), (-0.2, 0.2), (0.2, 0.5)]
            heights = [base_height, peak_height, base_height]
        elif num_intervals == 5:
            intervals = [(-0.5, -0.4), (-0.4, -0.2), (-0.2, 0.2), (0.2, 0.4), (0.4, 0.5)]
            heights = [base_height, base_height * 0.8, peak_height, base_height * 0.8, base_height]
        elif num_intervals == 7:
            intervals = [(-0.5, -0.4), (-0.4, -0.3), (-0.3, -0.2), (-0.2, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5)]
            heights = [base_height, base_height * 0.7, base_height * 0.9, peak_height, base_height * 0.9, base_height * 0.7, base_height]
        else:
            center = 0.0
            step_size = 0.5 / ((num_intervals - 1) / 2)
            for i in range(num_intervals // 2):
                left = -0.5 + i * step_size
                right = left + step_size
                intervals.append((left, right))
                if i == num_intervals // 2 - 1:
                    heights.append(peak_height)
                else:
                    heights.append(base_height + (peak_height - base_height) * 0.5)
            if num_intervals > 3:
                for i in range(num_intervals // 2 - 1, -1, -1):
                    intervals.append((-intervals[i][1], -intervals[i][0]))
                    heights.append(heights[i])
        
        f_code = "def create_step_function(x):\n    f = jnp.piecewise(x, [\n"
        for i, (start, end) in enumerate(intervals[:len(intervals) // 2 + (1 if num_intervals % 2 == 1 else 0)]):
            f_code += "        " + str(start) + " < x < " + str(end) + ",\n"
        f_code += "\n    ], [" + ", ".join([str(h) for h in heights[:len(intervals) // 2 + (1 if num_intervals % 2 == 1 else 0)]]) + ", 0.0])\n    return f\n"
    else:
        intervals = []
        heights = []
        num_peaks = min(num_intervals, 4)
        for i in range(num_peaks):
            center = random.uniform(-0.3, 0.3)
            width = random.uniform(0.15, 0.25)
            height = base_height + peak_height * random.uniform(0.3, 0.8)
            intervals.append((center - width / 2, center + width / 2))
            heights.append(height)
        
        while len(intervals) < num_intervals:
            if len(intervals) == 0:
                intervals.append((-0.5, -0.4))
                heights.append(0.0)
            else:
                intervals.append((intervals[-1][1], intervals[-1][1] + 0.1))
                heights.append(0.0)
        
        f_code = "def create_step_function(x):\n    f = jnp.piecewise(x, [\n"
        for i, (start, end) in enumerate(intervals):
            if i < len(intervals) - 1:
                f_code += "        " + str(start) + " < x < " + str(end) + ",\n"
            else:
                f_code += "        " + str(start) + " < x,\n"
        f_code += "\n    ], [" + ", ".join([str(h) for h in heights]) + ", 0.0])\n    return f\n"
    
    return {"type": "symmetric" if symmetric else "asymmetric", "num_intervals": num_intervals, "peak_height": peak_height, "function_code": f_code}
