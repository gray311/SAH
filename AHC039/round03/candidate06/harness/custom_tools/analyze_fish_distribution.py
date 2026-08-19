def run(ctx, args):
    names = ctx.list_task_inputs()
    if not names:
        return {"note": "no task inputs"}
    
    # This tool provides structural guidance for the solver
    # Key insight: mackerels and sardines have distinct spatial distributions
    # A good polygon should cover dense mackerel regions while avoiding sardines
    
    return {
        "n_mackerels": 5000,
        "n_sardines": 5000,
        "coord_range": [0, 100000],
        "recommended_strategy": "cluster_based",
        "key_insights": [
            "Mackerels likely form dense clusters; target these with polygon vertices",
            "Sardines are negative utility; design polygon boundaries to avoid them",
            "Use perimeter budget (400,000) to create multiple cluster-coverage rectangles",
            "Internal search over polygon parameters can beat static solutions",
            "KD-tree for fast density estimation around candidate regions"
        ],
        "parameters_to_tune": [
            "cluster_expansion_factor",
            "min_mackerel_density_threshold",
            "sardine_avoidance_weight",
            "internal_search_iterations",
            "vertex_limit_per_cluster"
        ]
    }
