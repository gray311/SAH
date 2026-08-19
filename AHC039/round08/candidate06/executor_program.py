# EVOLVE-BLOCK-START
"""
Focused search around mackerel clusters - very fast
"""

code = r'''#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdio>

const int MAX_COORD = 100000;
const int MAX_N = 5000;

struct Point { int x, y; };
struct Fish { Point p; int type; };

Fish fish_arr[10000];
int N_val = 0;

void count_in_rect(Point minp, Point maxp, int& m_cnt, int& s_cnt) {
    m_cnt = s_cnt = 0;
    for (int i = 0; i < 2 * N_val; i++) {
        const Fish& f = fish_arr[i];
        if (f.p.x >= minp.x && f.p.x <= maxp.x && f.p.y >= minp.y && f.p.y <= maxp.y) {
            if (f.type == 1) m_cnt++;
            else s_cnt++;
        }
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    
    int N_in;
    if (!(std::cin >> N_in)) return 0;
    N_val = N_in;
    
    for (int i = 0; i < N_val; i++) {
        std::cin >> fish_arr[i].p.x >> fish_arr[i].p.y;
        fish_arr[i].type = 1;
    }
    for (int i = 0; i < N_val; i++) {
        std::cin >> fish_arr[N_val + i].p.x >> fish_arr[N_val + i].p.y;
        fish_arr[N_val + i].type = -1;
    }
    
    int mnX = MAX_COORD, mnY = MAX_COORD, mxX = -1, mxY = -1;
    for (int i = 0; i < N_val; i++) {
        if (fish_arr[i].type == 1) {
            mnX = std::min(mnX, fish_arr[i].p.x);
            mnY = std::min(mnY, fish_arr[i].p.y);
            mxX = std::max(mxX, fish_arr[i].p.x);
            mxY = std::max(mxY, fish_arr[i].p.y);
        }
    }
    
    if (mnX > mxX || mnY > mxY) {
        printf("4\n0 0\n1 0\n1 1\n0 1\n");
        return 0;
    }
    
    int best_score = 0;
    std::vector<Point> best_poly;
    
    // Try 4 corners of mackerel bounding box with various sizes
    int cx_list[4] = {mnX, mxX, mxX, mnX};
    int cy_list[4] = {mxY, mxY, mnY, mnY};
    
    // Very limited search: 4 corners x 5 sizes = 20 candidates
    int sizes[] = {50, 100, 150, 250, 400};
    
    for (int c = 0; c < 4; c++) {
        for (int s = 0; s < 5; s++) {
            int cx = cx_list[c];
            int cy = cy_list[c];
            int sz = sizes[s];
            
            Point p[4];
            if (c == 0) { // TL
                p[0] = {cx, cy + sz}; p[1] = {cx + sz, cy + sz}; p[2] = {cx + sz, cy}; p[3] = {cx, cy};
            } else if (c == 1) { // TR
                p[0] = {cx - sz, cy + sz}; p[1] = {cx, cy + sz}; p[2] = {cx, cy}; p[3] = {cx - sz, cy};
            } else if (c == 2) { // BL
                p[0] = {cx, cy - sz}; p[1] = {cx + sz, cy - sz}; p[2] = {cx + sz, cy}; p[3] = {cx, cy};
            } else { // BR
                p[0] = {cx - sz, cy - sz}; p[1] = {cx, cy - sz}; p[2] = {cx, cy}; p[3] = {cx - sz, cy};
            }
            
            int min_x = std::max(mnX, std::min(mxX, p[0].x));
            int max_x = std::max(min_x, std::min(mxX, p[1].x));
            int min_y = std::max(mnY, std::min(mxY, std::min(p[0].y, p[2].y)));
            int max_y = std::max(min_y, std::min(mxY, std::max(p[0].y, p[3].y)));
            
            if (max_x > min_x && max_y > min_y) {
                int m = 0, s = 0;
                count_in_rect({min_x, min_y}, {max_x, max_y}, m, s);
                int sc = m - s + 1;
                if (sc > best_score) { best_score = sc; best_poly = {p[0], p[1], p[2], p[3]}; }
            }
        }
    }
    
    // Also try 3 random perturbations
    for (int r = 0; r < 3; r++) {
        int rx = mnX + (mxX - mnX) / 4 * r;
        int ry = mnY + (mxY - mnY) / 4 * r;
        
        for (int s = 0; s < 5; s++) {
            int sz = sizes[s];
            Point p[4];
            
            for (int c = 0; c < 4; c++) {
                if (c == 0) { p[0] = {rx, ry + sz}; p[1] = {rx + sz, ry + sz}; p[2] = {rx + sz, ry}; p[3] = {rx, ry}; }
                else if (c == 1) { p[0] = {rx - sz, ry + sz}; p[1] = {rx, ry + sz}; p[2] = {rx, ry}; p[3] = {rx - sz, ry}; }
                else if (c == 2) { p[0] = {rx, ry - sz}; p[1] = {rx + sz, ry - sz}; p[2] = {rx + sz, ry}; p[3] = {rx, ry}; }
                else { p[0] = {rx - sz, ry - sz}; p[1] = {rx, ry - sz}; p[2] = {rx, ry}; p[3] = {rx - sz, ry}; }
                
                int min_x = std::max(mnX, std::min(mxX, p[0].x));
                int max_x = std::max(min_x, std::min(mxX, p[1].x));
                int min_y = std::max(mnY, std::min(mxY, std::min(p[0].y, p[2].y)));
                int max_y = std::max(min_y, std::min(mxY, std::max(p[0].y, p[3].y)));
                
                if (max_x > min_x && max_y > min_y) {
                    int m = 0, s = 0;
                    count_in_rect({min_x, min_y}, {max_x, max_y}, m, s);
                    int sc = m - s + 1;
                    if (sc > best_score) { best_score = sc; best_poly = {p[0], p[1], p[2], p[3]}; }
                }
            }
        }
    }
    
    printf("%d\n", best_poly.size());
    for (const auto& pt : best_poly) {
        printf("%d %d\n", pt.x, pt.y);
    }
    
    return 0;
}
'''

CPP_CODE = code
# EVOLVE-BLOCK-END
