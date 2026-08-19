# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <set>
#include <cmath>
#include <numeric>
#include <map>

// === MACROS AND CONSTANTS ===
const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

// === RANDOM NUMBER GENERATION ===
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
    double next_double() { return next() / (double)UINT64_MAX; }
};
XorShift rng;

// === TIMER ===
struct Timer {
    std::chrono::steady_clock::time_point start_time;
    Timer() { reset(); }
    void reset() { start_time = std::chrono::steady_clock::now(); }
    double elapsed() const {
        auto now = std::chrono::steady_clock::now();
        return std::chrono::duration_cast<std::chrono::duration<double>>(now - start_time).count();
    }
};
Timer global_timer;

// === GEOMETRIC STRUCTURES ===
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
std::vector<Fish> all_fish;

// === POLYGON UTILITIES ===
long long calculate_perimeter(const std::vector<Point>& poly) {
    if (poly.size() < 2) return 0;
    long long perimeter = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        const Point& p1 = poly[i];
        const Point& p2 = poly[(i + 1) % poly.size()];
        perimeter += std::abs(p1.x - p2.x) + std::abs(p1.y - p2.y);
    }
    return perimeter;
}

bool is_on_segment(Point p, Point seg_a, Point seg_b) {
    if (p.x != seg_a.x && p.x != seg_b.x) return false;
    if (p.y != seg_a.y && p.y != seg_b.y) return false;
    return std::min(seg_a.x, seg_b.x) <= p.x && p.x <= std::max(seg_a.x, seg_b.x) &&
           std::min(seg_a.y, seg_b.y) <= p.y && p.y <= std::max(seg_a.y, seg_b.y);
}

bool is_inside_polygon(Point p, const std::vector<Point>& polygon) {
    int n = polygon.size();
    if (n < 3) return false;

    for (int i = 0; i < n; ++i) {
        if (is_on_segment(p, polygon[i], polygon[(i + 1) % n])) return true;
    }
    
    int wn = 0;
    for (int i = 0; i < n; ++i) {
        Point p1 = polygon[i];
        Point p2 = polygon[(i + 1) % n];
        if (p1.y <= p.y) {
            if (p2.y > p.y && (long long)(p2.x - p1.x) * (p.y - p1.y) > 0) {
                wn++;
            }
        } else {
            if (p2.y <= p.y && (long long)(p2.x - p1.x) * (p.y - p1.y) < 0) {
                wn--;
            }
        }
    }
    return wn != 0;
}

void calculate_score(const std::vector<Point>& poly, int& m_count, int& s_count) {
    m_count = 0; s_count = 0;
    if (poly.size() < 3) return;
    for (const auto& fish : all_fish) {
        if (is_inside_polygon(fish.p, poly)) {
            if (fish.type == 1) m_count++;
            else s_count++;
        }
    }
}

// Check self-intersection for orthogonal polygon
bool check_self_intersection(const std::vector<Point>& poly) {
    int M = poly.size();
    if (M < 4) return false;
    for (int i = 0; i < M; ++i) {
        Point p1s = poly[i];
        Point p1e = poly[(i + 1) % M];
        for (int j = i + 2; j < M; ++j) {
            if (i == 0 && j == M - 1) continue;
            Point p2s = poly[j];
            Point p2e = poly[(j + 1) % M];
            
            bool seg1_v = (p1s.x == p1e.x);
            bool seg2_v = (p2s.x == p2e.x);
            
            if (seg1_v == seg2_v) {
                if (seg1_v) {
                    if (p1s.x != p2s.x) continue;
                    int min1 = std::min(p1s.y, p1e.y), max1 = std::max(p1s.y, p1e.y);
                    int min2 = std::min(p2s.y, p2e.y), max2 = std::max(p2s.y, p2e.y);
                    if (std::max(min1, min2) <= std::min(max1, max2)) return true;
                } else {
                    if (p1s.y != p2s.y) continue;
                    int min1 = std::min(p1s.x, p1e.x), max1 = std::max(p1s.x, p1e.x);
                    int min2 = std::min(p2s.x, p2e.x), max2 = std::max(p2s.x, p2e.x);
                    if (std::max(min1, min2) <= std::min(max1, max2)) return true;
                }
            } else {
                Point v_s = seg1_v ? p1s : p2s;
                Point v_e = seg1_v ? p1e : p2e;
                Point h_s = seg1_v ? p2s : p1s;
                Point h_e = seg1_v ? p2e : p1e;
                
                int ix = v_s.x, iy = h_s.y;
                if (ix >= h_s.x && ix <= h_e.x && iy >= v_s.y && iy <= v_e.y) {
                    bool at_endpoint = (ix == v_s.x && iy == v_s.y) ||
                                      (ix == v_e.x && iy == v_e.y) ||
                                      (ix == h_s.x && iy == h_s.y) ||
                                      (ix == h_e.x && iy == h_e.y);
                    if (!at_endpoint) return true;
                }
            }
        }
    }
    return false;
}

bool has_distinct_vertices(const std::vector<Point>& poly) {
    if (poly.empty()) return true;
    std::set<Point> distinct_pts;
    for(const auto& p : poly) {
        if (!distinct_pts.insert(p).second) return false;
    }
    return true;
}

bool is_valid_polygon(const std::vector<Point>& poly) {
    int m = poly.size();
    if (m < 4 || m > MAX_VERTICES) return false;
    if (calculate_perimeter(poly) > MAX_PERIMETER) return false;
    
    for (size_t i = 0; i < m; ++i) {
        const Point& p1 = poly[i];
        const Point& p2 = poly[(i + 1) % m];
        if (p1.x < 0 || p1.x > MAX_COORD_VAL || p1.y < 0 || p1.y > MAX_COORD_VAL) return false;
        if (poly[(i+1)%m].x < 0 || poly[(i+1)%m].x > MAX_COORD_VAL || 
            poly[(i+1)%m].y < 0 || poly[(i+1)%m].y > MAX_COORD_VAL) return false;
        if (p1.x != p2.x && p1.y != p2.y) return false;
        if (p1.x == p2.x && p1.y == p2.y) return false;
    }
    return true;
}

// Create a larger initial polygon from multiple mackerels
std::vector<Point> create_initial_polygon() {
    // Find bounding box of first 10 mackerels
    int min_x = MAX_COORD_VAL, max_x = 0, min_y = MAX_COORD_VAL, max_y = 0;
    int count = 0;
    
    for (int i = 0; i < std::min(10, (int)all_fish.size()); ++i) {
        if (all_fish[i].type == 1) {
            min_x = std::min(min_x, all_fish[i].p.x);
            max_x = std::max(max_x, all_fish[i].p.x);
            min_y = std::min(min_y, all_fish[i].p.y);
            max_y = std::max(max_y, all_fish[i].p.y);
            count++;
        }
    }
    
    // Ensure valid bounds
    min_x = std::max(0, min_x);
    max_x = std::min(MAX_COORD_VAL, max_x);
    min_y = std::max(0, min_y);
    max_y = std::min(MAX_COORD_VAL, max_y);
    
    // Ensure non-degenerate
    if (min_x >= max_x) max_x = min_x + 1;
    if (min_y >= max_y) max_y = min_y + 1;
    
    std::vector<Point> poly = {
        {min_x, min_y}, {max_x, min_y}, {max_x, max_y}, {min_x, max_y}
    };
    return poly;
}

// Expand polygon in all 4 directions, keeping best
void expand_polygon(std::vector<Point>& poly, int max_expansion) {
    int best_m = 0, best_s = 0;
    calculate_score(poly, best_m, best_s);
    int best_score = std::max(0, best_m - best_s + 1);
    
    // Save original
    std::vector<Point> original = poly;
    
    for (int dir = 0; dir < 4; ++dir) {
        int dx = 0, dy = 0;
        if (dir == 0) dx = 1;
        else if (dir == 1) dy = 1;
        else if (dir == 2) dx = -1;
        else dy = -1;
        
        for (int step = 1; step <= max_expansion; ++step) {
            if (dir == 0) { poly[1].x = poly[2].x = std::min(poly[1].x + 1, MAX_COORD_VAL); }
            else if (dir == 1) { poly[1].y = poly[2].y = std::min(poly[1].y + 1, MAX_COORD_VAL); }
            else if (dir == 2) { poly[0].x = poly[3].x = std::max(poly[0].x - 1, 0); }
            else { poly[0].y = poly[3].y = std::max(poly[0].y - 1, 0); }
            
            if (!is_valid_polygon(poly) || check_self_intersection(poly)) {
                poly = original;
                break;
            }
            
            int m_count = 0, s_count = 0;
            calculate_score(poly, m_count, s_count);
            int score = std::max(0, m_count - s_count + 1);
            
            if (score > best_score) {
                best_score = score;
                best_m = m_count;
                best_s = s_count;
            }
        }
    }
    
    // Restore original if no improvement
    if (best_score <= std::max(0, best_m - best_s + 1)) {
        poly = original;
    }
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    int N;
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

    Timer t;
    t.reset();

    // Create initial polygon from multiple mackerels
    std::vector<Point> poly = create_initial_polygon();
    
    // Expand
    while (t.elapsed() < 1.8) {
        expand_polygon(poly, 100);
        if (t.elapsed() > 1.75) break;
    }

    if (!is_valid_polygon(poly) || check_self_intersection(poly) || !has_distinct_vertices(poly)) {
        poly = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
    }

    std::cout << poly.size() << "\\n";
    for (const auto& p : poly) {
        std::cout << p.x << " " << p.y << "\\n";
    }

    return 0;
}
'''
# EVOLVE-BLOCK-END
