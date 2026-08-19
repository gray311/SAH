def run(ctx, args):
    return {
        "trigger": "SWITCH_REQUIRED: Detected piecewise-linear tunneling",
        "action": "ABORT current optimization. Generate step function variants using generate_step_variants tool. Expected C2: 0.8963-0.905",
        "step_templates": [
            {"name": "canonical_step", "params": {"start_frac": 0.2, "end_frac": 0.8, "height": 1.0}},
            {"name": "tall_step", "params": {"start_frac": 0.25, "end_frac": 0.75, "height": 1.4}},
            {"name": "narrow_step", "params": {"start_frac": 0.3, "end_frac": 0.7, "height": 1.6}},
            {"name": "wide_step", "params": {"start_frac": 0.15, "end_frac": 0.85, "height": 0.8}},
            {"name": "asymmetric", "params": {"left": {"start": 0.15, "end": 0.4, "height": 2.0}, "right": {"start": 0.6, "end": 0.85, "height": 0.7}}}
        ],
        "rationale": "Step functions have demonstrated C2=0.8963. The seed's piecewise-linear is likely suboptimal. Switch IMMEDIATELY to explore step variants."
    }
