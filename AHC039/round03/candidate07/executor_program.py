# EVOLVE-BLOCK-START
CPP_CODE = """
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int N;
    std::cin >> N;
    
    std::vector<int> mx(N), my(N), sx(N), sy(N);
    
    for (int i = 0; i < N; i++) std::cin >> mx[i] >> my[i];
    for (int i = 0; i < N; i++) std::cin >> sx[i] >> sy[i];
    
    int GRID = 50;
    std::vector<std::vector<int>> g(GRID, std::vector<int>(GRID, 0));
    
    for (int i = 0; i < N; i++) {
        g[my[i]/(100000/GRID)][mx[i]/(100000/GRID)]++;
    }
    for (int i = 0; i < N; i++) {
        g[sy[i]/(100000/GRID)][sx[i]/(100000/GRID)]--;
    }
    
    int best = -999999999, br=0, bc=0;
    for (int r = 0; r < GRID; r++)
        for (int c = 0; c < GRID; c++)
            if (g[r][c] > best) { best = g[r][c]; br = r; bc = c; }
    
    int cs = 100000/GRID;
    int x1 = bc * cs, y1 = br * cs, x2 = (bc+1)*cs - 1, y2 = (br+1)*cs - 1;
    x1 = std::max(0, x1); y1 = std::max(0, y1);
    x2 = std::min(x2, 100000); y2 = std::min(y2, 100000);
    if (x1 > x2) std::swap(x1, x2);
    if (y1 > y2) std::swap(y1, y2);
    if (x1 == x2) x2++;
    if (y1 == y2) y2++;
    
    std::cout << 4 << \"\\\\n\";
    std::cout << x1 << \" \" << y1 << \"\\\\n\";
    std::cout << x2 << \" \" << y1 << \"\\\\n\";
    std::cout << x2 << \" \" << y2 << \"\\\\n\";
    std::cout << x1 << \" \" << y2 << \"\\\\n\";
    
    return 0;
}
"""
# EVOLVE-BLOCK-END
