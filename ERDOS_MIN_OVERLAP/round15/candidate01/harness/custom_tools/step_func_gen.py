def run(ctx, args):
    import numpy as np
    functions = {}
    
    # Binary: h = 1 on [0, 0.5]
    functions['binary_0_5'] = {
        'intervals': [(0.0, 0.5), (0.5, 2.0)],
        'heights': [2.0, 0.0],
        'description': 'h=1 on [0,0.5], h=0 elsewhere. integral=1.0'
    }
    
    # Binary shifted: h = 1 on [0.25, 0.75]
    functions['binary_0_25_0_75'] = {
        'intervals': [(0.0, 0.25), (0.25, 0.75), (0.75, 2.0)],
        'heights': [0.0, 4.0, 0.0],
        'description': 'h=1 on [0.25,0.75], h=0 elsewhere'
    }
    
    # Three-part: high-low-high pattern
    functions['three_part'] = {
        'intervals': [(0.0, 0.33), (0.33, 0.66), (0.66, 2.0)],
        'heights': [3.0, 0.0, 1.0],
        'description': 'h=3 on [0,0.33], h=0 on [0.33,0.66], h=1 on [0.66,2]'
    }
    
    # Asymmetric three-part
    functions['asymmetric_three'] = {
        'intervals': [(0.0, 0.5), (0.5, 1.5), (1.5, 2.0)],
        'heights': [2.0, 0.0, 2.0],
        'description': 'h=2 on [0,0.5], h=0 on [0.5,1.5], h=2 on [1.5,2]'
    }
    
    # Two-level with different weights
    functions['two_level_weighted'] = {
        'intervals': [(0.0, 0.4), (0.4, 1.0), (1.0, 2.0)],
        'heights': [2.5, 0.0, 2.5],
        'description': 'h=2.5 on [0,0.4], h=0 on [0.4,1.0], h=2.5 on [1.0,2]'
    }
    
    # Five-part symmetric
    functions['five_part_sym'] = {
        'intervals': [(0.0, 0.3), (0.3, 0.4), (0.4, 0.6), (0.6, 0.7), (0.7, 2.0)],
        'heights': [3.33, 0.0, 3.33, 0.0, 1.0],
        'description': 'symmetric five-part pattern'
    }
    
    # Six-part with 3 peaks
    functions['six_part_3peaks'] = {
        'intervals': [(0.0, 0.25), (0.25, 0.33), (0.33, 0.5), (0.5, 0.66), (0.66, 0.75), (0.75, 2.0)],
        'heights': [4.0, 0.0, 4.0, 0.0, 4.0, 1.0],
        'description': 'three peaks at 0.25, 0.5, 0.66'
    }
    
    # Seven-part fine-grained
    functions['seven_part'] = {
        'intervals': [(0.0, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 2.0)],
        'heights': [5.0, 0.0, 5.0, 0.0, 5.0, 0.0, 2.0],
        'description': 'seven intervals with three peaks'
    }
    
    # Simple uniform: h=0.5 everywhere
    functions['uniform'] = {
        'intervals': [(0.0, 2.0)],
        'heights': [0.5],
        'description': 'h=0.5 constant. integral=1.0. C5 will be 0.5.'
    }
    
    # Golden ratio split: h=1.618 on [0, 0.618], h=0 elsewhere
    functions['golden'] = {
        'intervals': [(0.0, 0.618), (0.618, 2.0)],
        'heights': [1.618, 0.0],
        'description': 'Golden ratio split: h=1.618 on [0,0.618]'
    }
    
    # Triangle-like: high-medium-low-medium-high
    functions['triangle_like'] = {
        'intervals': [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.2)],
        'heights': [5.0, 0.0, 5.0, 0.0, 5.0],
        'description': 'triangle-like with 3 peaks'
    }
    
    return {"step_functions": functions, "count": len(functions)}
