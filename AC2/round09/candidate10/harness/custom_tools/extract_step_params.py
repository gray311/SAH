def run(ctx, args):
    code = ctx.get_program()
    lines = code.split('\n')
    heights = []
    fractions = []
    step_count = 0
    in_creator = False
    
    for i, line in enumerate(lines):
        if '_create_step_initializer' in line:
            in_creator = True
            continue
        if in_creator:
            if '.set(' in line:
                # Extract height value
                import re
                match = re.search(r'\.(set\(\[?\s*([\d.]+)', line)
                if match:
                    heights.append(float(match.group(1)))
                    step_count += 1
            if 'int(' in line and '*' in line and '*' not in ''.join(lines[max(0,i-10):i]):
                # Extract fractions like int(0.25 * n)
                matches = re.findall(r'int\((\d+\.\d+)?\s*\*\s*n\)', line)
                fractions.extend([float(f) for f in matches])
            if 'f = jnp.zeros' in line or 'return' in line:
                in_creator = False
    
    return {
        "peak_heights": heights[:10],  # First 10 unique heights
        "interval_fractions": sorted(set(fractions)),
        "num_steps": step_count,
        "note": "Use these to guide your next edit"
    }
