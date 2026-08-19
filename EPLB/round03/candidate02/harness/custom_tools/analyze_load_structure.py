import re

def run(ctx, args):
    # Get the current program source
    lines = ctx.get_program().split('\n')
    # Parse tensor shape from a weight.shape() call
    weight_shape = None
    heavy_experts = []
    n_layers = None
    n_experts = None
    for line in lines:
        match = re.search(r'weight\.shape\s*=\s*(\[\s*\d+\s*,\s*\d+\s*\])', line)
        if match:
            weight_shape = match.group(1)
            n_layers = weight_shape.split(',')[0].strip('[]').strip()
            n_experts = weight_shape.split(',')[-1].strip()
    return {"n_layers": n_layers, "n_experts": n_experts,
            "analysis": "Check weight distribution for imbalance indicators"}