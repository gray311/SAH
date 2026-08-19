# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>

const int MAX_COORD = 100000;
const int MAX_VERT = 1000;
const int MAX_P = 400000;

struct P { int x, y; };
struct F { P p; int t; };

std::vector<F> fish;
int grid[256][256];
const int CG = 400;

void build_grid() {
    for (auto& f : fish) {
        int c = f.p.x / CG, r = f.p.y / CG;
        c = std::max(0, std::min(255, c)); r = std::max(0, std::min(255, r));
        grid[r][c] += f.t;
    }
}

int verify_count(int x1, int y1, int x2, int y2) {
    int m = 0, s = 0;
    for (auto& f : fish) {
        if (f.p.x >= x1 && f.p.x <= x2 && f.p.y >= y1 && f.p.y <= y2) {
            if (f.t == 1) m++; else s++;
        }
    }
    return m - s;
}

long long perim(const std::vector<P>& poly) {
    long long p = 0;
    int n = poly.size();
    for (int i = 0; i < n; i++) {
        p += std::abs(poly[i].x - poly[(i+1)%n].x) + std::abs(poly[i].y - poly[(i+1)%n].y);
    }
    return p;
}

std::vector<P> solve() {
    std::vector<P> best; int bests = -2e9;
    
    std::vector<std::pair<int, int>> cells;
    for (int r = 0; r < 256; r++) {
        for (int c = 0; c < 256; c++) {
            cells.push_back({grid[r][c], r * 256 + c});
        }
    }
    std::sort(cells.begin(), cells.end(), std::greater<std::pair<int, int>>());
    
    std::vector<int> Xcand, Ycand;
    for (size_t i = 0; i < cells.size() && i < 3000; i++) {
        int r = cells[i].second / 256;
        int c = cells[i].second % 256;
        Xcand.push_back(c * CG);
        Xcand.push_back((c + 1) * CG);
        Ycand.push_back(r * CG);
        Ycand.push_back((r + 1) * CG);
    }
    Xcand.push_back(0); Xcand.push_back(MAX_COORD);
    Ycand.push_back(0); Ycand.push_back(MAX_COORD);
    
    std::sort(Xcand.begin(), Xcand.end());
    Xcand.erase(std::unique(Xcand.begin(), Xcand.end()), Xcand.end());
    std::sort(Ycand.begin(), Ycand.end());
    Ycand.erase(std::unique(Ycand.begin(), Ycand.end()), Ycand.end());
    
    int sx = std::min(100, (int)Xcand.size());
    int sy = std::min(100, (int)Ycand.size());
    int limit = 2500000;
    
    for (int i = 0; i < sx && limit > 0; i++) {
        for (int j = i; j < sx && limit > 0; j++) {
            if (Xcand[i] == Xcand[j]) continue;
            for (int k = 0; k < sy && limit > 0; k++) {
                for (int l = k; l < sy && limit > 0; l++) {
                    if (Ycand[k] == Ycand[l]) continue;
                    
                    int x1 = Xcand[i], x2 = Xcand[j], y1 = Ycand[k], y2 = Ycand[l];
                    if (x2 - x1 < 50 || y2 - y1 < 50) {
                        limit--; continue;
                    }
                    
                    int est = 0, cx1=x1/CG, cy1=y1/CG, cx2=x2/CG, cy2=y2/CG;
                    for (int r=cy1; r<=cy2; r++) for (int c=cx1; c<=cx2; c++) est += grid[r][c];
                    
                    if (est + 1 <= bests) {
                        limit--; continue;
                    }
                    
                    limit--;
                    int sc = verify_count(x1, y1, x2, y2);
                    if (sc + 1 > bests) {
                        bests = sc + 1;
                        best = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
                    }
                }
            }
        }
    }
    
    if (best.empty() || bests <= 0) {
        best = {{0,0}, {1,0}, {1,1}, {0,1}};
        bests = 1;
    }
    
    if (perim(best) > MAX_P) {
        best = {{0,0}, {50000,0}, {50000,50000}, {0,50000}};
    }
    
    return best;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N; std::cin >> N;
    fish.resize(2 * N);
    
    for (int i = 0; i < N; i++) {
        std::cin >> fish[i].p.x >> fish[i].p.y;
        fish[i].t = 1;
    }
    for (int i = 0; i < N; i++) {
        std::cin >> fish[N+i].p.x >> fish[N+i].p.y;
        fish[N+i].t = -1;
    }
    
    build_grid();
    std::vector<P> p = solve();
    
    std::cout << p.size() << "\\n";
    for (auto& x : p) std::cout << x.x << " " << x.y << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
