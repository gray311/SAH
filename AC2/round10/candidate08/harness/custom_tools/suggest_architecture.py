def run(ctx, args):
    import random
    import re

    prog = ctx.get_program()
    heights = []
    h_matches = re.findall(r'\.set\((\d+\.\d+)\)', prog)
    if h_matches:
        try:
            heights = [float(h) for h in h_matches[:5]]
        except:
            heights = []

    if heights and all(0.8 <= h <= 2.8 for h in heights):
        arch_types = [
            ("ultra-narrow-spike", "Width 15-25%, height 3-5, central spike"),
            ("bi-modal", "Two 16-20% peaks with 40% gap, height 2.0-3.0 each"),
            ("asymmetric-cascade", "25% rise, 10% sharp peak (3.5), 15% decay"),
            ("plateau-shoulders", "15% shoulder, 50% plateau (2.5), 15% shoulder"),
            ("tri-modal", "Three 10% peaks with 20% gaps, height 1.8-2.5"),
        ]
        random.shuffle(arch_types)
        return {
            "recommendation": "FORCE architecture change - you are in seed basin",
            "current_heights": heights,
            "suggest_try_first": arch_types[0][0],
            "description": arch_types[0][1],
            "example": arch_types[0][0]
        }
    else:
        return {
            "recommendation": "Continue with current architecture or try alternative",
            "current_heights": heights,
            "suggest_try_first": "maintain",
            "description": "Heights suggest you may be exploring new space",
            "example": "no change needed"
        }
