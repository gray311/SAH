# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

const int MAX_COORD = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct Point {
    int x, y;
};

struct Fish {
    Point p;
    int type;
};

vector<Fish> fish_list;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    fish_list.resize(2 * N);
    for (int i = 0; i < N; i++) {
        cin >> fish_list[i].p.x >> fish_list[i].p.y;
        fish_list[i].type = 1;
    }
    for (int i = 0; i < N; i++) {
        cin >> fish_list[N + i].p.x >> fish_list[N + i].p.y;
        fish_list[N + i].type = -1;
    }
    
    if (fish_list.empty()) {
        cout << "4" << endl;
        cout << "0 0" << endl;
        cout << "1 0" << endl;
        cout << "1 1" << endl;
        cout << "0 1" << endl;
        return 0;
    }
    
    vector<Point> best_poly = {{0,0}, {1,0}, {1,1}, {0,1}};
    int best_score = -1e9;
    
    // Find bounding box of all fish
    int min_x = MAX_COORD, max_x = 0, min_y = MAX_COORD, max_y = 0;
    for (const auto& f : fish_list) {
        min_x = min(min_x, f.p.x);
        max_x = max(max_x, f.p.x);
        min_y = min(min_y, f.p.y);
        max_y = max(max_y, f.p.y);
    }
    
    if (min_x > max_x || min_y > max_y) {
        cout << "4" << endl;
        cout << "0 0" << endl;
        cout << "1 0" << endl;
        cout << "1 1" << endl;
        cout << "0 1" << endl;
        return 0;
    }
    
    // Try different grid sizes
    for (int grid_size : {50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100}) {
        int num_cells_x = (max_x - min_x) / grid_size + 1;
        int num_cells_y = (max_y - min_y) / grid_size + 1;
        
        for (int by = 0; by < num_cells_y && by < 80; by++) {
            for (int bx = 0; bx < num_cells_x && bx < 80; bx++) {
                if (by * num_cells_x + bx >= 1600) break;
                
                int x1 = min_x + bx * grid_size;
                int y1 = min_y + by * grid_size;
                int x2 = min(x1 + grid_size, max_x + 1);
                int y2 = min(y1 + grid_size, max_y + 1);
                
                if (x1 >= x2 || y1 >= y2) continue;
                
                vector<Point> poly = {{x1,y1}, {x2,y1}, {x2,y2}, {x1,y2}};
                
                int m_cnt = 0, s_cnt = 0;
                for (const auto& f : fish_list) {
                    if (f.p.x >= x1 && f.p.x < x2 && f.p.y >= y1 && f.p.y < y2) {
                        if (f.type == 1) m_cnt++;
                        else s_cnt++;
                    }
                }
                
                int score = m_cnt - s_cnt + 1;
                if (score > best_score) {
                    best_score = score;
                    best_poly = poly;
                }
            }
        }
    }
    
    // Expand outward in all 4 directions with multiple margins
    vector<Point> poly = best_poly;
    int m_cnt = 0, s_cnt = 0;
    for (const auto& f : fish_list) {
        if (f.p.x >= poly[0].x && f.p.x < poly[1].x &&
            f.p.y >= poly[0].y && f.p.y < poly[2].y) {
            if (f.type == 1) m_cnt++;
            else s_cnt++;
        }
    }
    int current_score = m_cnt - s_cnt + 1;
    
    // Try multiple expansion margins
    for (int margin : {50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000}) {
        vector<Point> candidates[4];
        // Expand right
        candidates[0] = {{poly[0].x, poly[0].y}, {poly[1].x + margin, poly[0].y}, 
                         {poly[1].x + margin, poly[2].y}, {poly[0].x, poly[2].y}};
        // Expand left
        candidates[1] = {{poly[0].x - margin, poly[0].y}, {poly[0].x, poly[0].y}, 
                         {poly[0].x, poly[2].y}, {poly[0].x - margin, poly[2].y}};
        // Expand up
        candidates[2] = {{poly[0].x, poly[0].y}, {poly[1].x, poly[0].y}, 
                         {poly[1].x, poly[2].y + margin}, {poly[0].x, poly[2].y + margin}};
        // Expand down
        candidates[3] = {{poly[0].x, poly[0].y - margin}, {poly[1].x, poly[0].y - margin}, 
                         {poly[1].x, poly[0].y}, {poly[0].x, poly[0].y}};
        
        for (int dir = 0; dir < 4; dir++) {
            vector<Point> cand = candidates[dir];
            for (auto& p : cand) {
                if (p.x < 0) p.x = 0;
                if (p.y < 0) p.y = 0;
            }
            
            m_cnt = 0; s_cnt = 0;
            for (const auto& f : fish_list) {
                if (f.p.x >= cand[0].x && f.p.x < cand[1].x &&
                    f.p.y >= cand[0].y && f.p.y < cand[2].y) {
                    if (f.type == 1) m_cnt++;
                    else s_cnt++;
                }
            }
            int score = m_cnt - s_cnt + 1;
            if (score > current_score) {
                current_score = score;
                poly = cand;
            }
        }
    }
    
    cout << poly.size() << endl;
    for (const auto& p : poly) {
        cout << p.x << " " << p.y << endl;
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
