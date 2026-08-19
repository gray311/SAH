# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <climits>

const int MAX_COORD = 100000;
const int GRID_SIZE = 1000;
const int CELL_SIZE = 100;
const int MAX_PERIMETER = 400000;
const int MAX_VERTICES = 1000;

struct Fish { int x, y, type; };

int grid[GRID_SIZE][GRID_SIZE];
int prefix_sum[GRID_SIZE][GRID_SIZE];

void build_grid(const std::vector<Fish>& fish) {
    for (int i = 0; i < GRID_SIZE; i++)
        for (int j = 0; j < GRID_SIZE; j++) grid[i][j] = 0;
    for (const auto& f : fish) {
        int cx = f.x / CELL_SIZE, cy = f.y / CELL_SIZE;
        cx = std::min(std::max(0, cx), GRID_SIZE - 1);
        cy = std::min(std::max(0, cy), GRID_SIZE - 1);
        grid[cy][cx] += f.type;
    }
}

void compute_prefix_sums() {
    for (int i = 0; i < GRID_SIZE; i++) {
        for (int j = 0; j < GRID_SIZE; j++) {
            prefix_sum[i][j] = grid[i][j];
            if (i > 0) prefix_sum[i][j] += prefix_sum[i-1][j];
            if (j > 0) prefix_sum[i][j] += prefix_sum[i][j-1];
            if (i > 0 && j > 0) prefix_sum[i][j] -= prefix_sum[i-1][j-1];
        }
    }
}

int query(int x1, int y1, int x2, int y2) {
    if (x1 > x2 || y1 > y2) return 0;
    int cx1 = std::max(0, x1 / CELL_SIZE), cx2 = std::min(x2 / CELL_SIZE, GRID_SIZE - 1);
    int cy1 = std::max(0, y1 / CELL_SIZE), cy2 = std::min(y2 / CELL_SIZE, GRID_SIZE - 1);
    if (cx1 > cx2 || cy1 > cy2) return 0;
    int res = prefix_sum[cy2][cx2];
    if (cx1 > 0) res -= prefix_sum[cy2][cx1 - 1];
    if (cy1 > 0) res -= prefix_sum[cy1 - 1][cx2];
    if (cx1 > 0 && cy1 > 0) res += prefix_sum[cy1 - 1][cx1 - 1];
    return res;
}

struct BestPoly { std::vector<std::pair<int,int>> v; };
BestPoly best;

int main() {
    int N; std::cin >> N;
    std::vector<Fish> f(2*N);
    for (int i = 0; i < N; i++) { std::cin >> f[i].x >> f[i].y; f[i].type = 1; }
    for (int i = 0; i < N; i++) { std::cin >> f[N+i].x >> f[N+i].y; f[N+i].type = -1; }
    
    build_grid(f); compute_prefix_sums();
    best.v = {{0,0},{1,0},{1,1},{0,1}};
    
    std::vector<int> cx_list, cy_list;
    cx_list.push_back(0); cx_list.push_back(GRID_SIZE);
    cy_list.push_back(0); cy_list.push_back(GRID_SIZE);
    for (const auto& fl : f) {
        int cx = fl.x / CELL_SIZE, cy = fl.y / CELL_SIZE;
        cx_list.push_back(cx); cx_list.push_back(cx+1);
        cy_list.push_back(cy); cy_list.push_back(cy+1);
    }
    std::sort(cx_list.begin(), cx_list.end());
    cx_list.erase(std::unique(cx_list.begin(), cx_list.end()), cx_list.end());
    std::sort(cy_list.begin(), cy_list.end());
    cy_list.erase(std::unique(cy_list.begin(), cy_list.end()), cy_list.end());
    
    // Limit search space but try more combinations
    int n = std::min((int)cx_list.size(), 80);
    
    for (int i = 0; i < n && i < (int)cx_list.size(); i++) {
        for (int j = i; j < n && j < (int)cx_list.size(); j++) {
            int x1 = cx_list[i] * CELL_SIZE, x2 = cx_list[j] * CELL_SIZE + CELL_SIZE;
            if (x2 - x1 > MAX_PERIMETER/2) continue;
            
            int cur = 0, mx = 0, by1 = 0, by2 = 0;
            for (size_t k = 0; k < cy_list.size(); k++) {
                int y = cy_list[k] * CELL_SIZE;
                int sc = query(x1, y, x2, y + CELL_SIZE);
                cur += sc;
                if (cur > mx) { mx = cur; by1 = y; by2 = y + CELL_SIZE; }
                if (cur < 0) cur = 0;
            }
            if (mx > best.v.size()) {
                long long per = 2LL * (x2 - x1 + by2 - by1);
                if (per <= MAX_PERIMETER) {
                    best.v = {{x1, by1}, {x2, by1}, {x2, by2}, {x1, by2}};
                }
            }
        }
    }
    
    std::cout << best.v.size() << "\\n";
    for (auto& p : best.v) std::cout << p.first << " " << p.second << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
