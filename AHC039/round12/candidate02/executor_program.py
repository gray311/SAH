# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <set>
#include <cmath>
#include <cstdlib>

const int MAX_COORD = 100000;
const int MAX_VERT = 1000;
const int MAX_PERIM = 400000;
const int MAX_REST = 14;

struct Point { int x, y; };
struct Fish { Point p; int type; };

std::vector<Fish> fish_list;

int calc_score(const std::vector<Point>& poly) {
    if (poly.size() < 4) return 0;
    int M = 0, S = 0;
    for (const auto& f : fish_list) {
        bool inside = false;
        for (size_t i = 0; i < poly.size(); ++i) {
            const Point& p1 = poly[i];
            const Point& p2 = poly[(i + 1) % poly.size()];
            if ((p1.y > f.p.y) != (p2.y > f.p.y)) {
                double x_int = p2.x - (p2.x - p1.x) * (f.p.y - p1.y) / (p2.y - p1.y);
                if (f.p.x < x_int) { inside = true; break; }
            }
        }
        if (inside) { if (f.type == 1) M++; else S++; }
    }
    return M - S + 1;
}

bool is_valid(const std::vector<Point>& poly) {
    if (poly.size() < 4 || poly.size() > MAX_VERT) return false;
    long long perm = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        perm += std::abs(poly[i].x - poly[(i+1)%poly.size()].x) + std::abs(poly[i].y - poly[(i+1)%poly.size()].y);
        if (perm > MAX_PERIM) return false;
    }
    return true;
}

void quick_hill_climb(std::vector<Point>& poly) {
    int best_score = calc_score(poly);
    for (int pass = 0; pass < 2; ++pass) {
        bool improved = true;
        while (improved) {
            improved = false;
            std::vector<Point> best_poly = poly;
            int best_s = best_score;
            for (size_t i = 0; i < poly.size(); ++i) {
                Point p = poly[i];
                for (int s = 1; s <= 12; s += 2) {
                    int dx = (rand() % (2 * s)) - s;
                    int dy = (rand() % (2 * s)) - s;
                    if (dx == 0 && dy == 0) continue;
                    p.x += dx; p.y += dy;
                    if (p.x < 0 || p.x > MAX_COORD || p.y < 0 || p.y > MAX_COORD) continue;
                    poly[i] = p;
                    int s_new = calc_score(poly);
                    if (s_new > best_s) {
                        best_s = s_new;
                        improved = true;
                        best_poly = poly;
                    }
                    poly[i] = Point(poly[(i+1)%poly.size()].x, poly[(i+1)%poly.size()].y);
                }
                poly[i] = best_poly[i];
            }
            poly = best_poly;
            best_score = best_s;
        }
    }
}

std::vector<Point> make_rect(Point c, int r) {
    int x1 = std::max(0, c.x - r);
    int x2 = std::min(MAX_COORD, c.x + r);
    int y1 = std::max(0, c.y - r);
    int y2 = std::min(MAX_COORD, c.y + r);
    std::vector<Point> rect;
    rect.reserve(4);
    rect.push_back({x1, y1});
    rect.push_back({x2, y1});
    rect.push_back({x2, y2});
    rect.push_back({x1, y2});
    return rect;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    
    int N; std::cin >> N;
    fish_list.resize(2 * N);
    
    for (int i = 0; i < N; ++i) {
        std::cin >> fish_list[i].p.x >> fish_list[i].p.y; fish_list[i].type = 1;
    }
    for (int i = 0; i < N; ++i) {
        std::cin >> fish_list[N + i].p.x >> fish_list[N + i].p.y; fish_list[N + i].type = -1;
    }
    
    std::mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count());
    double limit = 1.8;
    auto start_time = std::chrono::steady_clock::now();
    
    std::vector<Point> global_best;
    int best_score = 0;
    
    for (int rest = 0; rest < MAX_REST; ++rest) {
        auto now = std::chrono::steady_clock::now();
        if (std::chrono::duration_cast<std::chrono::milliseconds>(now - start_time).count() / 1000.0 > limit) break;
        
        for (int t = 0; t < 4; ++t) {
            Point c = fish_list[std::uniform_int_distribution<>(0, 2*N - 1)(rng)].p;
            int r = std::max(15, std::min(c.x, c.y) + 5 + rand() % 20);
            std::vector<Point> poly = make_rect(c, r);
            
            quick_hill_climb(poly);
            int s = calc_score(poly);
            if (is_valid(poly) && s > best_score) {
                best_score = s;
                global_best = poly;
            }
        }
    }
    
    if (global_best.empty()) global_best = {{0,0}, {100,0}, {100,100}, {0,100}};
    
    std::cout << global_best.size() << "\\n";
    for (const auto& p : global_best) std::cout << p.x << " " << p.y << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
