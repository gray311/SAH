def run(ctx, args):
    code = ctx.get_program()
    lines = code.split('\n')
    issues = []
    op_estimate = 0
    for i, line in enumerate(lines):
        if 'for p in range' in line or '[p for p' in line:
            issues.append("Line {}: Python loop, slow".format(i))
            op_estimate += 1000
        if '.item()' in line or '.tolist()' in line:
            issues.append("Line {}: Python conversion, slow".format(i))
            op_estimate += 200
    return {
        "bottlenecks": issues[:5],
        "estimated_ops": op_estimate,
        "recommendation": "Replace with torch.scatter or gather if bottlenecks found"
    }
