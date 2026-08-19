# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

const int MAX_COORD = 100000;

struct Point { int x, y; };

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int N;
    cin >> N;
    
    vector<Point> mackerels(N), sardines(N);
    for (int i = 0; i < N; i++) cin >> mackerels[i].x >> mackerels[i].y;
    for (int i = 0; i < N; i++) cin >> sardines[i].x >> sardines[i].y;
    
    auto score_rect = [&](int lx, int rx, int ly, int ry) -> int {
        int m = 0, s = 0;
        for (int i = 0; i < N; i++) {
            if (mackerels[i].x >= lx && mackerels[i].x <= rx && mackerels[i].y >= ly && mackerels[i].y <= ry) m++;
        }
        for (int i = 0; i < N; i++) {
            if (sardines[i].x >= lx && sardines[i].x <= rx && sardines[i].y >= ly && sardines[i].y <= ry) s++;
        }
        return m - s;
    };
    
    vector<Point> best_poly = {{0,0}, {1,0}, {1,1}, {0,1}};
    int best_score = 1;
    
    // Find all candidate cluster centers
    vector<int> candidates;
    for (int i = 0; i < N; i++) {
        int cnt = 0;
        for (int j = 0; j < N; j++) {
            int dx = mackerels[i].x - mackerels[j].x;
            int dy = mackerels[i].y - mackerels[j].y;
            if (dx*dx + dy*dy < 400000) cnt++;
        }
        if (cnt >= 10) candidates.push_back(i);
    }
    
    // 150 restarts - more iterations
    unsigned int seed = 42;
    
    for (int r = 0; r < 150; r++) {
        seed += r * 31;
        
        int cidx = candidates[r % candidates.size()];
        int cx = mackerels[cidx].x, cy = mackerels[cidx].y;
        
        // Try multiple radii
        int rad = 500000 + (r % 9) * 100000;
        
        int min_x = MAX_COORD, max_x = 0, min_y = MAX_COORD, max_y = 0;
        for (int i = 0; i < N; i++) {
            int dx = mackerels[i].x - cx;
            int dy = mackerels[i].y - cy;
            if (dx*dx + dy*dy < rad) {
                min_x = min(min_x, mackerels[i].x);
                max_x = max(max_x, mackerels[i].x);
                min_y = min(min_y, mackerels[i].y);
                max_y = max(max_y, mackerels[i].y);
            }
        }
        
        if (min_x > max_x) { min_x = cx - 350; max_x = cx + 350; }
        if (min_y > max_y) { min_y = cy - 350; max_y = cy + 350; }
        if (min_x < 0) min_x = 0; if (min_y < 0) min_y = 0;
        if (max_x > MAX_COORD) max_x = MAX_COORD; if (max_y > MAX_COORD) max_y = MAX_COORD;
        
        vector<Point> poly = {{min_x, min_y}, {max_x, min_y}, {max_x, max_y}, {min_x, max_y}};
        
        int cur_sc = score_rect(min_x, max_x, min_y, max_y);
        
        // Even deeper optimization
        for (int iter = 0; iter < 20; iter++) {
            for (int e = 0; e < 4; e++) {
                for (int off : {-5,-10,-15,-20,-25,-30,5,10,15,20,25,30}) {
                    if (seed % 100 > 20) continue;
                    seed += 37;
                    
                    vector<Point> cand = poly;
                    Point p1 = cand[e], p2 = cand[(e+1)%4];
                    int dx = p2.x - p1.x, dy = p2.y - p1.y;
                    int new_c = dx == 0 ? p1.x + off : p1.y + off;
                    if (new_c < 0 || new_c > MAX_COORD) continue;
                    
                    if (dx == 0) { cand[e].x = new_c; cand[(e+1)%4].x = new_c; }
                    else { cand[e].y = new_c; cand[(e+1)%4].y = new_c; }
                    
                    int nx = min({cand[0].x, cand[1].x, cand[2].x, cand[3].x});
                    int mx = max({cand[0].x, cand[1].x, cand[2].x, cand[3].x});
                    int ny = min({cand[0].y, cand[1].y, cand[2].y, cand[3].y});
                    int my = max({cand[0].y, cand[1].y, cand[2].y, cand[3].y});
                    
                    if (nx > mx || ny > my) continue;
                    
                    int ns = score_rect(nx, mx, ny, my);
                    if (ns > cur_sc) {
                        poly = cand; min_x = nx; max_x = mx; min_y = ny; max_y = my;
                        cur_sc = ns;
                        best_score = max(best_score, ns + 1);
                        break;
                    }
                }
                if (cur_sc >= 0) break;
            }
        }
        
        int final_sc = score_rect(min_x, max_x, min_y, max_y);
        if (final_sc + 1 > best_score) { best_score = final_sc + 1; best_poly = poly; }
    }
    
    cout << best_poly.size() << "\n";
    for (const auto& p : best_poly) cout << p.x << " " << p.y << "\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
