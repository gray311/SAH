def run(ctx, args):
    program = ctx.get_program()
    best_score = ctx.best_score()
    
    analysis = """
    STEP FUNCTION ANALYSIS:
    
    Why C2 ≈ 0.8963 is achieved:
    - Step functions create sharp transitions in f(x)
    - This leads to concentrated ||f★f||_∞ (peak value is high)
    - The L2 norm ||f★f||₂ is also substantial due to flat regions
    - The ratio ||f★f||₂² / (||f★f||₁ ||f★f||_∞) is optimized
    
    Weak points to exploit:
    1. SHARPNESS LIMIT: Steps are too sharp - smooth transitions can improve ||f★f||₂
       without increasing ||f★f||_∞ proportionally.
    2. SYMMETRY: Current steps may be symmetric; asymmetric shapes break constructive interference.
    3. MODALITY: Single-modal step functions; multi-modal functions can create
       structured convolutions with better L2/L∞ ratios.
    4. CONTINUITY: Discontinuities in f(x) create issues; smooth functions avoid these.
    
    RECOMMENDED FAMILIES:
    - Gaussian mixtures: Multi-modal smooth functions
    - B-splines: Flexible smooth transitions
    - Piecewise-linear: Controlled smoothness
    - Oscillatory decay: Structured convolutions
    - Multi-level sharp: 4-6 levels with asymmetric heights
    """
    
    return {"analysis": analysis, "key_insights": ["multi-modality helps", "smooth transitions beneficial", "asymmetry breaks symmetry", "probe before evaluate"],
            "recommended_families": ["gaussian_mixture", "bspline", "piecewise_linear", "oscillatory_decay", "multi_level_sharp"]}
