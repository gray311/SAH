# EVOLVE-BLOCK-START
CPP_CODE = R'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cmath>

const int MAXC = 100000;
const int MAXV = 1000;
const int MAXP = 400000;

struct Fish { int x, y, t; };
std::vector<Fish> fish;
int N;

int count_rect(int x1, int y1, int x2, int y2) {
    int m = 0, s = 0;
    for (const auto& f : fish) {
        if (f.x >= x1 && f.x <= x2 && f.y >= y1 && f.y <= y2) {
            if (f.t == 1) m++;
            else s++;
        }
    }
    return std::max(0, m - s + 1);
}

std::vector<int> get_fish_stats(int x1, int y1, int x2, int y2) {
    std::vector<int> stats(2);
    for (const auto& f : fish) {
        if (f.x >= x1 && f.x <= x2 && f.y >= y1 && f.y <= y2) {
            if (f.t == 1) stats[0]++;
            else stats[1]++;
        }
    }
    return stats;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cin >> N;
    
    fish.clear();
    fish.resize(2 * N);
    
    std::vector<int> mx, my;
    for (int i = 0; i < N; i++) { 
        std::cin >> fish[i].x >> fish[i].y; 
        fish[i].t = 1;
        mx.push_back(fish[i].x);
        my.push_back(fish[i].y);
    }
    for (int i = 0; i < N; i++) { 
        std::cin >> fish[N+i].x >> fish[N+i].y; 
        fish[N+i].t = -1;
    }
    
    // Find mackerel bounding box
    int min_x = MAXC, max_x = 0, min_y = MAXC, max_y = 0;
    for (int i = 0; i < N; i++) {
        min_x = std::min(min_x, fish[i].x);
        max_x = std::max(max_x, fish[i].x);
        min_y = std::min(min_y, fish[i].y);
        max_y = std::max(max_y, fish[i].y);
    }
    
    // Generate many candidate rectangles
    std::vector<std::vector<int>> candidates;
    
    // Fixed patterns
    for (int base : {0, 25000, 50000, 75000}) {
        for (int sz : {25000, 50000}) {
            int x2 = std::min(base + sz, MAXC);
            int y2 = std::min(base + sz, MAXC);
            candidates.push_back({base, base, x2, y2});
            candidates.push_back({base, 0, x2, y2});
            candidates.push_back({0, base, x2, y2});
        }
    }
    
    // Mackerel-focused rectangles
    candidates.push_back({min_x, min_y, max_x, max_y});
    for (int pad : {10000, 20000, 30000, 40000}) {
        int x1 = std::max(0, min_x - pad);
        int y1 = std::max(0, min_y - pad);
        int x2 = std::min(MAXC, max_x + pad);
        int y2 = std::min(MAXC, max_y + pad);
        candidates.push_back({x1, y1, x2, y2});
    }
    
    // Quarter-based rectangles
    for (int qx : {0, 25000, 50000, 75000}) {
        for (int qy : {0, 25000, 50000, 75000}) {
            for (int qx2 : {25000, 50000, 75000, 100000}) {
                for (int qy2 : {25000, 50000, 75000, 100000}) {
                    candidates.push_back({qx, qy, qx2, qy2});
                }
            }
        }
    }
    
    // Find best
    int best_score = 0;
    std::vector<int> best_rect = {0, 0, 50000, 50000};
    
    for (const auto& r : candidates) {
        int score = count_rect(r[0], r[1], r[2], r[3]);
        if (score > best_score) {
            best_score = score;
            best_rect = r;
        }
    }
    
    // Local optimization: try small adjustments to best rectangle
    for (int adj_x : {-10000, 0, 10000}) {
        for (int adj_y : {-10000, 0, 10000}) {
            for (int adj_x2 : {-10000, 0, 10000}) {
                for (int adj_y2 : {-10000, 0, 10000}) {
                    int x1 = best_rect[0] + adj_x;
                    int y1 = best_rect[1] + adj_y;
                    int x2 = best_rect[2] + adj_x2;
                    int y2 = best_rect[3] + adj_y2;
                    
                    x1 = std::max(0, std::min(MAXC, x1));
                    y1 = std::max(0, std::min(MAXC, y1));
                    x2 = std::max(0, std::min(MAXC, x2));
                    y2 = std::max(0, std::min(MAXC, y2));
                    
                    int score = count_rect(x1, y1, x2, y2);
                    if (score > best_score) {
                        best_score = score;
                        best_rect = {x1, y1, x2, y2};
                    }
                }
            }
        }
    }
    
    std::cout << "4" << "\n";
    std::cout << best_rect[0] << " " << best_rect[1] << "\n";
    std::cout << best_rect[2] << " " << best_rect[1] << "\n";
    std::cout << best_rect[2] << " " << best_rect[3] << "\n";
    std::cout << best_rect[0] << " " << best_rect[3] << "\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
