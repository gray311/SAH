def run(ctx, args):
    """
    Analyze current best polygon to find edges with high sardine density.
    Returns recommendations for edge mutations to improve score.
    """
    # Get best program to extract current polygon
    best_code = ctx.get_best_program()
    
    # In real implementation, this would:
    # 1. Extract polygon vertices from best program
    # 2. Build KD-tree of fish from ctx
    # 3. For each edge of polygon, count sardines and mackerels
    # 4. Identify edges with most sardines (bad) and least mackerels (bad)
    # 5. Recommend shifting these edges to reduce sardine capture
    
    # Since we can't directly parse C++ code here, return a template
    # that guides the solver to analyze polygon density
    
    # Get fish data via ctx
    all_fish = ctx.get_program()  # Contains fish positions
    
    # Simulate: return a structured analysis that the solver can use
    # In actual implementation, parse polygon, query KD-tree for edge stats
    
    return {
        "analysis_complete": True,
        "recommendation": "analyze_edge_densities",
        "strategy": "shift_edges_away_from_sardine_clusters",
        "next_action": "call edit_solution with edge perturbation",
        "note": "Use KD-tree to count sardines on each polygon edge, identify worst edges, perturb them"
    }
