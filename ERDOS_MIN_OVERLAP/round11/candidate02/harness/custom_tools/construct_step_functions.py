def run(ctx, args):
    import numpy as np
    results = {}
    
    # 1. Uniform: h(x) = 0.5 everywhere
    results['uniform'] = {
        'breakpoints': [0.0, 2.0],
        'heights': [0.5]
    }
    
    # 2. Two-step left-heavy: h=1 on [0,a], h=0 elsewhere, integral=1 => a=1
    results['two_step_left'] = {
        'breakpoints': [0.0, 1.0, 2.0],
        'heights': [1.0, 0.0]
    }
    
    # 3. Two-step right-heavy: h=1 on [1,2]
    results['two_step_right'] = {
        'breakpoints': [0.0, 1.0, 2.0],
        'heights': [0.0, 1.0]
    }
    
    # 4. Three-step centered: high in middle, zero at edges
    # h=1 on [0.5,1.5], integral=1*1=1
    results['three_step_centered'] = {
        'breakpoints': [0.0, 0.5, 1.5, 2.0],
        'heights': [0.0, 1.0, 0.0]
    }
    
    # 5. Four-step even: 1 on [0,0.5] and [1,1.5]
    # integral = 0.5*1 + 0.5*1 = 1
    results['four_step_even'] = {
        'breakpoints': [0.0, 0.5, 1.0, 1.5, 2.0],
        'heights': [1.0, 0.0, 1.0, 0.0]
    }
    
    # 6. Weighted two-step: h=a on [0,1], h=b on (1,2], a+b=2
    results['weighted_two_step'] = {
        'breakpoints': [0.0, 1.0, 2.0],
        'heights': [1.2, 0.8]
    }
    
    # 7. Bimodal: two peaks at 1/3 and 2/3
    results['bimodal_steps'] = {
        'breakpoints': [0.0, 1/3, 2/3, 1.0],
        'heights': [1.5, 0.0, 1.5]
    }
    
    # 8. Triple peak: peaks at 1/4, 1/2, 3/4
    # h=2 on [0,1/4], h=0 on (1/4,1/2], h=2 on [1/2,3/4], h=0 on (3/4,2]
    # integral = 2*0.25 + 0 + 2*0.25 + 0 = 1
    results['triple_peak_steps'] = {
        'breakpoints': [0.0, 0.25, 0.5, 0.75, 1.0],
        'heights': [2.0, 0.0, 2.0, 0.0]
    }
    
    return {"constructions": results, "count": len(results)}