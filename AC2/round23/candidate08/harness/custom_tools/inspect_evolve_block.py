def run(ctx, args):
    import re
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    num_intervals = 600
    step_type = 'unknown'
    peak_count = 1
    for line in lines:
        if 'num_intervals' in line:
            match = re.search(r'num_intervals\s*=\s*(\d+)', line)
            if match:
                num_intervals = int(match.group(1))
        if 'start =' in line or 'end =' in line:
            if step_type == 'unknown':
                step_type = 'step-function'
        if 'height' in line.lower():
            match = re.search(r'height\s*=\s*([\d.]+)', line, re.IGNORECASE)
            if match:
                height = float(match.group(1))
                if height >= 2.0:
                    peak_count += 1
    return {'num_intervals': num_intervals, 'step_type': step_type, 'peak_count': peak_count}
