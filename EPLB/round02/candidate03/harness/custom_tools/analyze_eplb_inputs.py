def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"error": "no task inputs found"}
    # Take the largest input file as the weight matrix
    names_sorted = sorted(names, key=len)
    input_name = names_sorted[-1]
    df = ctx.read_input_df(input_name, nrows=10000)
    if df.empty:
        return {"error": "input file is empty or not parseable"}
    try:
        rows, cols = df.shape
        # Infer parameters from the data
        # The weight matrix is [num_moe_layers, num_logical_experts]
        num_moe_layers = rows
        num_logical_experts = cols
        # Assume num_groups is a divisor of num_logical_experts (e.g., 2, 4, 8)
        num_groups = 8
        num_logical_experts_div = num_logical_experts // num_groups
        # Estimate num_nodes from typical vLLM configs
        num_nodes = 2
        # Extract statistics
        weight_stats = df.describe(include='number').to_dict()
        mean_vals = [float(w) for w in weight_stats['mean'][:cols]]
        min_vals = [float(w) for w in weight_stats['min'][:cols]]
        max_vals = [float(w) for w in weight_stats['max'][:cols]]
        std_vals = [float(w) for w in weight_stats['std'][:cols]]
        return {
            "num_moe_layers": num_moe_layers,
            "num_logical_experts": num_logical_experts,
            "num_groups": num_groups,
            "num_nodes": num_nodes,
            "device": "cuda",
            "weight_stats": {
                "mean": mean_vals[:10],
                "min": min_vals[:10],
                "max": max_vals[:10],
                "std": std_vals[:10]
            },
            "total_elements": rows * cols
        }
    except Exception as e:
        return {"error": str(e)}
