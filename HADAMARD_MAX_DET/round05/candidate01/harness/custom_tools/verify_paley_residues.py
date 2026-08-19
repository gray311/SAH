def run(ctx, args):
    import re
    matrix_text = ctx.get_best_program()
    residues_match = re.search(r'residues\s*=\s*\{([^}]+)\}', matrix_text, re.IGNORECASE)
    if residues_match:
        residues_str = residues_match.group(1)
        try:
            residues = set(int(x.strip()) for x in residues_str.split() if x.strip().isdigit())
            correct_residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
            if residues == correct_residues:
                return {
                    "correct": True,
                    "residues_used": sorted(list(residues)),
                    "message": "Paley residues are CORRECT"
                }
            else:
                missing = correct_residues - residues
                extra = residues - correct_residues
                return {
                    "correct": False,
                    "residues_used": sorted(list(residues)),
                    "missing_residues": sorted(list(missing)),
                    "extra_residues": sorted(list(extra)),
                    "message": "WRONG RESIDUES! Missing: " + str(missing) + ", Extra: " + str(extra)
                }
        except Exception as e:
            return {"error": "Could not parse residues: " + str(e), "correct": False}
    else:
        return {
            "correct": False,
            "message": "Could not find residues set in your code. Ensure Paley construction uses: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}"
        }
