def run(ctx, args):
    import json
    import math
    
    vertices = args.get('vertices', [])
    direction = args.get('direction', 'E')
    shift_amount = args.get('shift_amount', 20)
    
    if not vertices:
        return {'error': 'No vertices provided'}
    
    # Get current program to estimate fish positions
    program_text = ctx.get_program()
    
    # Simple heuristic: assume vertices define a rectangle
    if len(vertices) >= 4:
        xs = [v['x'] for v in vertices]
        ys = [v['y'] for v in vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Try shifting in requested direction
        new_rect = {
            'min_x': min_x, 'max_x': max_x,
            'min_y': min_y, 'max_y': max_y
        }
        
        if direction == 'N':
            new_rect['min_y'] -= shift_amount
        elif direction == 'S':
            new_rect['min_y'] += shift_amount
        elif direction == 'E':
            new_rect['max_x'] += shift_amount
        elif direction == 'W':
            new_rect['max_x'] -= shift_amount
        
        # Clamp to valid range
        new_rect['min_x'] = max(0, min(new_rect['min_x'], new_rect['max_x']))
        new_rect['max_x'] = max(0, min(new_rect['max_x'], 100000))
        new_rect['min_y'] = max(0, min(new_rect['min_y'], new_rect['max_y']))
        new_rect['max_y'] = max(0, min(new_rect['max_y'], 100000))
        
        # Estimate improvement based on expansion area
        original_area = (new_rect['max_x'] - new_rect['min_x']) * (new_rect['max_y'] - new_rect['min_y'])
        new_area = (new_rect['max_x'] - new_rect['min_x']) * (new_rect['max_y'] - new_rect['min_y'])
        expansion = new_area - original_area
        
        # Heuristic: larger expansion likely captures more fish
        # But could also capture more sardines (negative impact)
        # Assume 1/5 expansion is beneficial mackerels, 1/20 is sardines
        estimated_mackerels = int(expansion / 5)
        estimated_sardines = int(expansion / 20)
        estimated_score = estimated_mackerels - estimated_sardines
        
        return {
            'refined_vertices': [
                {'x': new_rect['min_x'], 'y': new_rect['min_y']},
                {'x': new_rect['max_x'], 'y': new_rect['min_y']},
                {'x': new_rect['max_x'], 'y': new_rect['max_y']},
                {'x': new_rect['min_x'], 'y': new_rect['max_y']}
            ],
            'estimated_improvement': estimated_score,
            'direction_applied': direction
        }
    
    return {'error': 'Need at least 4 vertices'}
