def run(ctx, args):
    import re
    import math
    from collections import defaultdict
    
    best_program = ctx.get_best_program()
    current_c2 = ctx.best_score()
    
    proposals = []
    
    # Propose refined step functions (baseline improvement)
    proposals.append({
        "type": "refined_step",
        "description": "Multi-level step with asymmetric heights and split peaks",
        "config": {
            "base": "step",
            "variations": [
                {"levels": 5, "asymmetric": True, "split_peak": True},
                {"levels": 3, "wings": True, "peak_ratio": 0.7},
                {"levels": 4, "staircase": True, "gradient": 0.2}
            ]
        },
        "edit_hint": "Use f.at[start:end].set(value) for multiple segments"
    })
    
    # Propose Gaussian mixture
    proposals.append({
        "type": "gaussian_mixture",
        "description": "2-3 component Gaussian mixture with softplus weights",
        "config": {
            "base": "gaussian_mixture",
            "components": 2,
            "weight_transform": "softplus",
            "width_range": (0.1, 1.0),
            "center_constraints": "symmetric or bimodal"
        },
        "edit_hint": "Sum of Gaussians: f(x) = sum(w_i * exp(-((x-u_i)/s_i)^2))"
    })
    
    # Propose B-spline
    proposals.append({
        "type": "bspline",
        "description": "B-spline with 5-7 knots, polynomial pieces",
        "config": {
            "base": "bspline",
            "knots": 6,
            "degree": 3,
            "knot_distribution": "clustered"
        },
        "edit_hint": "Use scipy.interpolate.BSpline or custom B-spline basis"
    })
    
    # Propose hybrid
    proposals.append({
        "type": "hybrid_step_gaussian",
        "description": "Step function with Gaussian decay tails",
        "config": {
            "base": "hybrid",
            "core": "step",
            "tails": "gaussian_decay",
            "transition_width": 0.15
        },
        "edit_hint": "Step in center, Gaussian exp(-((x-a)/s)^2) on edges"
    })
    
    # Add context about current architecture
    proposals.append({
        "type": "context",
        "description": f"Current best c2: {current_c2:.6f}",
        "recommendation": "Try architectural diversity - do not refine same family"
    })
    
    return {"proposals": proposals, "count": len(proposals)}
