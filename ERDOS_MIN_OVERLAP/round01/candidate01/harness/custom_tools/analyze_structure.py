def run(ctx, args):
    prog = ctx.get_program()
    num_intervals = 200
    penalty_strength = 1000000.0
    lines = prog.strip().split('\n')
    for line in lines:
        if 'num_intervals:' in line:
            parts = [x.strip() for x in line.split('=') if x.strip()]
            if len(parts) >= 2:
                try:
                    num_intervals = int(parts[1])
                except:
                    pass
        if 'penalty_strength:' in line:
            parts = [x.strip() for x in line.split('=') if x.strip()]
            if len(parts) >= 2:
                try:
                    penalty_strength = float(parts[1])
                except:
                    pass
    if num_intervals < 100:
        recommended = num_intervals * 3
    elif num_intervals < 200:
        recommended = 250
    elif num_intervals < 400:
        recommended = 500
    else:
        recommended = num_intervals * 2
    diag = []
    diag.append(f"Current config: num_intervals={num_intervals}, penalty_strength={penalty_strength:.0f}")
    diag.append(f"Recommended num_intervals: {recommended}")
    if penalty_strength < 100000:
        diag.append("Penalty strength too low - constraint likely violated")
    elif penalty_strength > 10000000:
        diag.append("Penalty strength very high - may cause optimization instability")
    else:
        diag.append("Penalty strength appears reasonable")
    if num_intervals < 150:
        diag.append("Consider coarse-to-fine: start coarse, then refine")
    diag.append("\nSuggested strategy: Try num_intervals=50-100 first for quick results,")
    diag.append("then refine to 200-500 if coarse solutions work well.")
    return {
        "num_intervals": num_intervals,
        "penalty_strength": penalty_strength,
        "recommended_intervals": recommended,
        "diagnosis": "\n".join(diag)
    }
