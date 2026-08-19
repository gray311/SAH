def run(ctx, args):
    pattern = args.get("pattern", "nested_loops")
    func_name = args.get("function_name", "")
    
    transformations = {
        "nested_loops": "Use torch.sort and slice assignment instead of for loops. Compute indices with torch.arange and assign via modulo.",
        "min_finding": "Replace min(pack_weights) with torch.argmin(pack_weights, dim=0).",
        "accumulation": "Use torch.scatter_add for accumulation instead of Python loop.",
        "packing": "Sort weights with torch.sort(-1, descending=True), then assign using modulo: pack_index = sorted_indices % num_packs."
    }
    
    if pattern in transformations:
        return {"pattern": pattern, "transformation": transformations[pattern]}
    return {"error": "Unknown pattern"}
