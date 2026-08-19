# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <set>
#include <unordered_set>
#include <cmath>
#include <iomanip>
#include <numeric>
#include <string>
#include <map>
#include <cstring>

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
    int type;
};

std::vector<Fish> all_fish;
int N;

int score_polygon(const std::vector<Point>& poly) {
    int m_count = 0, s_count = 0;
    if (poly.size() < 3) return 0;
    for (const auto& fish : all_fish) {
        bool inside = false;
        for (size_t i = 0, j = poly.size() - 1; i < poly.size(); j = i++) {
            if (((poly[i].y > fish.p.y) != (poly[j].y > fish.p.y)) &&
                (fish.p.x < (double)(poly[j].x - poly[i].x) * (fish.p.y - poly[i].y) / (poly[i].y - poly[j].y) + poly[i].x)) {
                inside = !inside;
            }
        }
        if (inside) {
            if (fish.type == 1) m_count++;
            else s_count++;
        }
    }
    return std::max(0, m_count - s_count + 1);
}

struct XorShift {
    uint64_t x;
    XorShift() : x(std::chrono::steady_clock::now().time_since_epoch().count() ^ ((uint64_t)std::random_device()() << 32) ^ std::random_device()()) {}
    uint64_t next() {
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        return x;
    }
    int next_int(int n) { if (n <= 0) return 0; return next() % n; }
    int next_int(int a, int b) { if (a > b) return a; return a + next_int(b - a + 1); } 
};
XorShift rng;

int main(int argc, char *argv[]) {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    double time_limit = 1.9;
    if (argc > 1) { 
        try {
            time_limit = std::stod(argv[1]);
        } catch (...) {}
    }
    time_limit -= 0.1;
    if (time_limit < 0.2) time_limit = 0.2;

    std::cin >> N; 

    all_fish.resize(2 * N);
    
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[i].p.x >> all_fish[i].p.y;
        all_fish[i].type = 1; 
    }
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[N + i].p.x >> all_fish[N + i].p.y;
        all_fish[N + i].type = -1; 
    }
    
    // Find mackerel bounding box
    int min_x = MAX_COORD_VAL, max_x = 0;
    int min_y = MAX_COORD_VAL, max_y = 0;
    
    for (const auto& fish : all_fish) {
        if (fish.type == 1) {
            min_x = std::min(min_x, fish.p.x);
            max_x = std::max(max_x, fish.p.x);
            min_y = std::min(min_y, fish.p.y);
            max_y = std::max(max_y, fish.p.y);
        }
    }
    
    min_x -= 50; max_x += 50;
    min_y -= 50; max_y += 50;
    min_x = std::max(0, min_x); max_x = std::min(MAX_COORD_VAL, max_x);
    min_y = std::max(0, min_y); max_y = std::min(MAX_COORD_VAL, max_y);
    
    if (min_x >= max_x || min_y >= max_y) {
        min_x = 0; min_y = 0; max_x = 100; max_y = 100;
    }
    
    std::vector<Point> best_poly = {{min_x, min_y}, {max_x, min_y}, {max_x, max_y}, {min_x, max_y}};
    int best_score = score_polygon(best_poly);
    
    // Try notches and L-cuts
    for (int restart = 0; restart < 15; restart++) {
        std::vector<Point> poly = best_poly;
        
        // Try adding notches
        for (int v = 0; v < 50; v++) {
            std::vector<Point> var_poly = poly;
            
            if (var_poly.size() >= 4) {
                int edge_idx = rng.next_int((int)var_poly.size());
                int notch_width = rng.next_int(20, 100);
                int notch_depth = rng.next_int(50, 150);
                
                Point p1 = var_poly[edge_idx];
                Point p2 = var_poly[(edge_idx + 1) % var_poly.size()];
                
                std::vector<Point> new_poly = var_poly;
                if (p1.x != p2.x) {
                    int new_y = std::max(0, std::min(MAX_COORD_VAL, p1.y + notch_depth));
                    int notch_x1 = std::max(0, p1.x - notch_width / 2);
                    int notch_x2 = std::min(MAX_COORD_VAL, p2.x + notch_width / 2);
                    new_poly.insert(new_poly.begin() + (edge_idx + 1), {notch_x1, new_y});
                    new_poly.insert(new_poly.begin() + (edge_idx + 2), {notch_x2, new_y});
                } else {
                    int new_x = std::max(0, std::min(MAX_COORD_VAL, p1.x + notch_depth));
                    int notch_y1 = std::max(0, p1.y - notch_width / 2);
                    int notch_y2 = std::min(MAX_COORD_VAL, p2.y + notch_width / 2);
                    new_poly.insert(new_poly.begin() + (edge_idx + 1), {new_x, notch_y1});
                    new_poly.insert(new_poly.begin() + (edge_idx + 2), {new_x, notch_y2});
                }
                
                int score = score_polygon(new_poly);
                if (score > best_score) {
                    best_score = score;
                    best_poly = new_poly;
                }
            }
        }
        
        // Try L-cuts
        for (int corner = 0; corner < 4; corner++) {
            std::vector<Point> var_poly = best_poly;
            int cut_depth = rng.next_int(50, 150);
            
            Point p1 = var_poly[corner];
            Point p2 = var_poly[(corner + 1) % var_poly.size()];
            
            std::vector<Point> new_poly = var_poly;
            int new_x1 = std::max(0, p1.x + cut_depth);
            int new_y1 = std::max(0, p1.y + cut_depth);
            new_poly.insert(new_poly.begin() + (corner + 1), {new_x1, p1.y});
            new_poly.insert(new_poly.begin() + (corner + 2), {p2.x, new_y1});
            
            int score = score_polygon(new_poly);
            if (score > best_score) {
                best_score = score;
                best_poly = new_poly;
            }
        }
    }
    
    // Final refinement
    for (int iter = 0; iter < 20; iter++) {
        for (size_t i = 0; i < best_poly.size(); i++) {
            int dx = rng.next_int(-10, 10);
            int dy = rng.next_int(-10, 10);
            
            if (dx == 0 && dy == 0) continue;
            
            std::vector<Point> new_poly = best_poly;
            Point np = new_poly[i];
            np.x = std::max(0, std::min(MAX_COORD_VAL, np.x + dx));
            np.y = std::max(0, std::min(MAX_COORD_VAL, np.y + dy));
            new_poly[i] = np;
            
            int score = score_polygon(new_poly);
            if (score > best_score) {
                best_score = score;
                best_poly = new_poly;
            }
        }
    }
    
    std::cout << best_poly.size() << "\\n";
    for (const auto& p : best_poly) {
        std::cout << p.x << " " << p.y << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
