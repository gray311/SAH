def run(ctx, args):
    residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
    n = 29
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            offset = (i - j) % n
            if offset in residues:
                row.append(1)
            else:
                row.append(-1)
        matrix.append(row)
    return {"matrix": matrix, "n": n, "note": "Correct Paley with Legendre symbol"}
