# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <numeric>
#include <iomanip>

// === MACROS AND CONSTANTS ===
const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct Point {
    int x, y;
    bool operator<(const Point& other) const { 
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

struct Fish {
    Point p;
    int type; // 1 for mackerel, -1 for sardine
};

std::vector<Fish> all_fish_structs;

// === CALCULATE SCORE FOR RECTANGLE ===
int calculate_rectangle_score(int l, int r, int b, int t) {
    if (r <= l || t <= b) return -1e9;
    int m_count = 0, s_count = 0;
    for (const auto& fish : all_fish_structs) {
        if (fish.p.x >= l && fish.p.x <= r && fish.p.y >= b && fish.p.y <= t) {
            if (fish.type == 1) m_count++;
            else s_count++;
        }
    }
    return m_count - s_count + 1;
}

// === OPTIMIZE RECTANGLE SIZE ===
void create_optimal_rectangle(Point& center, int& w, int& h) {
    // Compute centroid
    long long sum_x = 0, sum_y = 0;
    for (const auto& fish : all_fish_structs) {
        sum_x += fish.p.x;
        sum_y += fish.p.y;
    }
    int cx = static_cast<int>(sum_x / all_fish_structs.size());
    int cy = static_cast<int>(sum_y / all_fish_structs.size());
    
    // Sample coordinates around the centroid
    std::set<int> x_coords, y_coords;
    for (const auto& fish : all_fish_structs) {
        for (int dx = -5; dx <= 5; ++dx) {
            x_coords.insert(std::max(0, std::min(MAX_COORD_VAL, fish.p.x + dx)));
        }
        for (int dy = -5; dy <= 5; ++dy) {
            y_coords.insert(std::max(0, std::min(MAX_COORD_VAL, fish.p.y + dy)));
        }
    }
    x_coords.insert(0);
    x_coords.insert(MAX_COORD_VAL);
    y_coords.insert(0);
    y_coords.insert(MAX_COORD_VAL);
    
    std::vector<int> x_list(x_coords.begin(), x_coords.end());
    std::vector<int> y_list(y_coords.begin(), y_coords.end());
    
    // Try different rectangle sizes
    int best_score = -1e9;
    int best_w = 10000, best_h = 10000;
    
    // Try more aggressive rectangle sizes
    const int step = 500;
    for (int total_size = 20000; total_size <= 200000; total_size += step) {
        // Try square and aspect ratio variations
        int pw = std::min(total_size / 2, 40000);
        int ph = std::min(total_size - 2 * pw, 40000);
        
        if (2 * pw + 2 * ph > MAX_PERIMETER) continue;
        
        for (int ratio = 0; ratio <= 3; ++ratio) {
            int try_pw = pw;
            int try_ph = ph;
            if (ratio == 1) { try_pw = ph; try_ph = pw; }
            if (ratio == 2) { try_pw = ph / 2; try_ph = ph; }
            if (ratio == 3) { try_pw = ph / 3; try_ph = ph; }
            
            int r = cx + try_pw / 2;
            int l_rect = cx - try_pw / 2;
            int t = cy + try_ph / 2;
            int b = cy - try_ph / 2;
            
            l_rect = std::max(0, l_rect); r = std::min(MAX_COORD_VAL, r);
            b = std::max(0, b); t = std::min(MAX_COORD_VAL, t);
            
            if (r > l_rect && t > b) {
                int score = calculate_rectangle_score(l_rect, r, b, t);
                if (score > best_score) {
                    best_score = score;
                    best_w = r - l_rect;
                    best_h = t - b;
                    center.x = cx - best_w / 2;
                    center.y = cy - best_h / 2;
                }
            }
        }
    }
    
    w = best_w;
    h = best_h;
}

void output_rectangle(Point center, int w, int h) {
    int x1 = center.x;
    int y1 = center.y;
    int x2 = center.x + w;
    int y2 = center.y + h;
    
    std::cout << "4" << "\\n";
    std::cout << x1 << " " << y1 << "\\n";
    std::cout << x2 << " " << y1 << "\\n";
    std::cout << x2 << " " << y2 << "\\n";
    std::cout << x1 << " " << y2 << "\\n";
}

// === MAIN ===
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    std::cin >> N;
    
    all_fish_structs.resize(2 * N);
    
    // Read mackerels
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish_structs[i].p.x >> all_fish_structs[i].p.y;
        all_fish_structs[i].type = 1;
    }
    
    // Read sardines
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish_structs[N + i].p.x >> all_fish_structs[N + i].p.y;
        all_fish_structs[N + i].type = -1;
    }
    
    Point center;
    int w, h;
    create_optimal_rectangle(center, w, h);
    
    output_rectangle(center, w, h);
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
