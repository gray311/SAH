def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N  # 0.0025
    specs = {}
    
    # bimodal_sharp: Two sharp plateaus
    # Plateaus at [0.25, 0.375] and [0.625, 0.75], each width=0.125, height=1
    # integral = 0.125 + 0.125 = 0.25, will normalize to 1
    specs["bimodal_sharp"] = {
        "num_steps": 8,
        "positions": [0.0, 0.25, 0.375, 0.625, 0.75, 1.0, 1.5, 2.0],
        "values": [0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0],
        "integral_raw": 0.25
    }
    
    # triplateau: Three-level construction
    # Low [0,0.5]=0, Medium [0.5,1]=0.4, High [1,1.5]=1, Low [1.5,2]=0
    # integral = 0.5*0.4 + 0.5*1 = 0.7
    specs["triplateau"] = {
        "num_steps": 5,
        "positions": [0.0, 0.5, 1.0, 1.5, 2.0],
        "values": [0.0, 0.4, 1.0, 0.0, 0.0],
        "integral_raw": 0.7
    }
    
    # golomb_scaled: Based on optimal difference set [0,1,4,9,11]
    # Scaled marks at approximately 0, 0.5, 1.6, 2.0
    # Creating peaks at these locations
    specs["golomb_scaled"] = {
        "num_steps": 7,
        "positions": [0.0, 0.33, 0.66, 1.0, 1.33, 1.66, 2.0],
        "values": [0.5, 0.8, 0.8, 0.5, 0.2, 0.2, 0.0],
        "integral_raw": 0.75
    }
    
    # asym_steps: Asymmetric with one dominant block
    specs["asym_steps"] = {
        "num_steps": 4,
        "positions": [0.0, 0.4, 1.0, 2.0],
        "values": [0.5, 0.5, 0.15, 0.0],
        "integral_raw": 0.6
    }
    
    # block_construct: Large solid blocks
    specs["block_construct"] = {
        "num_steps": 4,
        "positions": [0.0, 0.5, 1.0, 2.0],
        "values": [0.5, 0.5, 0.2, 0.0],
        "integral_raw": 0.75
    }
    
    return {"specs": specs, "num_specs": 5}