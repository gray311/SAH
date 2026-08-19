# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <set>

const int MAX_COORD = 100000;
const int MAX_PERIM = 400000;
const int MAX_VERT = 1000;
double TIME_LIMIT = 1.95;

struct Point { int x, y; };
struct Fish { Point p; int type; };
std::vector<Fish> fish;

bool on_seg(Point p, Point a, Point b) {
    long long cp = (long long)(b.x - a.x) * (p.y - a.y) - (long long)(b.y - a.y) * (p.x - a.x);
    if (cp != 0) return false;
    return std::min(a.x, b.x) <= p.x && p.x <= std::max(a.x, b.x) &&
           std::min(a.y, b.y) <= p.y && p.y <= std::max(a.y, b.y);
}

bool in_poly(Point p, const std::vector<Point>& poly) {
    int n = poly.size();
    if (n < 3) return false;
    for (int i = 0; i < n; i++) if (on_seg(p, poly[i], poly[(i+1)%n])) return true;
    int wn = 0;
    for (int i = 0; i < n; i++) {
        Point a = poly[i], b = poly[(i+1)%n];
        if (a.y <= p.y) {
            if (b.y > p.y && (long long)(b.x - a.x) * (p.y - a.y) - (long long)(b.y - a.y) * (p.x - a.x) > 0) wn++;
        } else {
            if (b.y <= p.y && (long long)(b.x - a.x) * (p.y - a.y) - (long long)(b.y - a.y) * (p.x - a.x) < 0) wn--;
        }
    }
    return wn != 0;
}

long long perim(const std::vector<Point>& p) {
    long long tot = 0;
    for (size_t i = 0; i < p.size(); i++) tot += std::abs(p[i].x - p[(i+1)%p.size()].x) + std::abs(p[i].y - p[(i+1)%p.size()].y);
    return tot;
}

bool intersect(Point a, Point b, Point c, Point d) {
    long long d1 = (long long)(d.x - c.x) * (b.y - c.y) - (long long)(d.y - c.y) * (b.x - c.x);
    long long d2 = (long long)(a.x - b.x) * (d.y - c.y) - (long long)(a.y - b.y) * (d.x - c.x);
    long long d3 = (long long)(d.x - c.x) * (a.y - b.y) - (long long)(d.y - c.y) * (a.x - b.x);
    long long d4 = (long long)(a.x - b.x) * (c.y - b.y) - (long long)(a.y - b.y) * (c.x - b.x);
    if (((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))) return true;
    if (d1 == 0 && on_seg(c, a, b)) return true;
    if (d2 == 0 && on_seg(b, c, d)) return true;
    if (d3 == 0 && on_seg(d, a, b)) return true;
    if (d4 == 0 && on_seg(a, c, d)) return true;
    return false;
}

bool valid_poly(const std::vector<Point>& poly) {
    if (poly.size() < 4 || poly.size() > MAX_VERT) return false;
    if (perim(poly) > MAX_PERIM) return false;
    std::set<long long> seen;
    for (const auto& p : poly) seen.insert(p.x * 100001LL + p.y);
    if ((int)seen.size() != poly.size()) return false;
    for (size_t i = 0; i < poly.size(); i++) {
        if (poly[i].x < 0 || poly[i].x > MAX_COORD || poly[i].y < 0 || poly[i].y > MAX_COORD) return false;
        Point p2 = poly[(i+1)%poly.size()];
        if (p2.x < 0 || p2.x > MAX_COORD || p2.y < 0 || p2.y > MAX_COORD) return false;
        if (poly[i].x == p2.x && poly[i].y == p2.y) return false;
        if (poly[i].x != p2.x && poly[i].y != p2.y) return false;
    }
    for (int i = 0; i < (int)poly.size(); i++) {
        Point a = poly[i], b = poly[(i+1)%poly.size()];
        for (int j = i + 2; j < (int)poly.size(); j++) {
            if (i == 0 && j == (int)poly.size() - 1) continue;
            Point c = poly[j], d = poly[(j+1)%poly.size()];
            if (intersect(a, b, c, d)) return false;
        }
    }
    return true;
}

bool in_rect(Point p, int x1, int x2, int y1, int y2) {
    return p.x >= x1 && p.x <= x2 && p.y >= y1 && p.y <= y2;
}

int count_mack(const std::vector<Point>& poly) {
    int m = 0;
    if (poly.size() < 3) return 0;
    for (const auto& f : fish) if (in_poly(f.p, poly) && f.type == 1) m++;
    return m;
}

int count_sard(const std::vector<Point>& poly) {
    int s = 0;
    if (poly.size() < 3) return 0;
    for (const auto& f : fish) if (in_poly(f.p, poly) && f.type == -1) s++;
    return s;
}

int score_poly(const std::vector<Point>& poly) {
    return std::max(0, count_mack(poly) - count_sard(poly) + 1);
}

int score_rect(int x1, int x2, int y1, int y2) {
    int m = 0, s = 0;
    for (const auto& f : fish) {
        if (in_rect(f.p, x1, x2, y1, y2)) {
            if (f.type == 1) m++; else s++;
        }
    }
    return std::max(0, m - s + 1);
}

int main() {
    std::ios_base::sync_with_stdio(false); std::cin.tie(NULL);
    TIME_LIMIT -= 0.05;
    if (TIME_LIMIT < 0.2) TIME_LIMIT = 0.2;
    
    struct Timer { std::chrono::steady_clock::time_point t; Timer(){t = std::chrono::steady_clock::now();} double e(){auto n = std::chrono::steady_clock::now(); return std::chrono::duration_cast<std::chrono::duration<double>>(n - t).count();} };
    Timer tm;
    
    int N; std::cin >> N;
    fish.resize(2 * N);
    for (int i = 0; i < N; i++) { std::cin >> fish[i].p.x >> fish[i].p.y; fish[i].type = 1; }
    for (int i = 0; i < N; i++) { std::cin >> fish[N + i].p.x >> fish[N + i].p.y; fish[N + i].type = -1; }
    
    std::vector<Point> best = {{0,0}, {1,0}, {1,1}, {0,1}};
    int best_sc = 1;
    
    std::vector<int> X, Y;
    for (const auto& f : fish) { X.push_back(f.p.x); X.push_back(f.p.x-1); X.push_back(f.p.x+1); Y.push_back(f.p.y); Y.push_back(f.p.y-1); Y.push_back(f.p.y+1); }
    X.push_back(0); X.push_back(MAX_COORD); Y.push_back(0); Y.push_back(MAX_COORD);
    std::sort(X.begin(), X.end()); X.erase(std::unique(X.begin(), X.end()), X.end());
    std::sort(Y.begin(), Y.end()); Y.erase(std::unique(Y.begin(), Y.end()), Y.end());
    
    int x_idx = 0, y_idx = 0;
    
    while (tm.e() < TIME_LIMIT) {
        // Strategy 1: Various rectangles
        for (int iter = 0; iter < 700 && tm.e() < TIME_LIMIT; iter++) {
            x_idx = (x_idx + 1) % X.size();
            y_idx = (y_idx + 1) % Y.size();
            int x1 = X[x_idx], x2 = X[(x_idx + 40) % X.size()];
            int y1 = Y[y_idx], y2 = Y[(y_idx + 40) % Y.size()];
            if (x1 > x2) std::swap(x1, x2);
            if (y1 > y2) std::swap(y1, y2);
            if ((long long)(x2-x1+y2-y1)*2 > MAX_PERIM) continue;
            int sc = score_rect(x1, x2, y1, y2);
            if (sc > best_sc) { best = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}}; best_sc = sc; }
        }
        
        // Strategy 2: Larger rectangles
        for (int iter = 0; iter < 600 && tm.e() < TIME_LIMIT; iter++) {
            x_idx = (x_idx + 1) % X.size();
            y_idx = (y_idx + 1) % Y.size();
            int x1 = X[x_idx], x2 = X[(x_idx + 300) % X.size()];
            int y1 = Y[y_idx], y2 = Y[(y_idx + 300) % Y.size()];
            if (x1 > x2) std::swap(x1, x2);
            if (y1 > y2) std::swap(y1, y2);
            if ((long long)(x2-x1+y2-y1)*2 > MAX_PERIM) continue;
            int sc = score_rect(x1, x2, y1, y2);
            if (sc > best_sc) { best = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}}; best_sc = sc; }
        }
        
        // Strategy 3: Refine best rectangle edges
        if (best.size() == 4) {
            int m = 4;
            for (int i = 0; i < m && tm.e() < TIME_LIMIT; i++) {
                Point a = best[i], b = best[(i+1)%m];
                if (a.x == b.x) {
                    int cx = a.x;
                    for (int dy = -1500; dy <= 1500 && tm.e() < TIME_LIMIT; dy += 1) {
                        int ny = a.y + dy;
                        if (ny < 0 || ny > MAX_COORD) continue;
                        std::vector<Point> new_poly = {a, {cx, ny}, b};
                        if (new_poly.size() < 4) continue;
                        if (!valid_poly(new_poly)) continue;
                        int sc = score_poly(new_poly);
                        if (sc > best_sc) { best = new_poly; best_sc = sc; goto next_edge; }
                    }
                } else {
                    int cy = a.y;
                    for (int dx = -1500; dx <= 1500 && tm.e() < TIME_LIMIT; dx += 1) {
                        int nx = a.x + dx;
                        if (nx < 0 || nx > MAX_COORD) continue;
                        std::vector<Point> new_poly = {a, {nx, cy}, b};
                        if (new_poly.size() < 4) continue;
                        if (!valid_poly(new_poly)) continue;
                        int sc = score_poly(new_poly);
                        if (sc > best_sc) { best = new_poly; best_sc = sc; goto next_edge; }
                    }
                }
                next_edge:;
            }
        }
    }
    
    std::cout << best.size() << "\\n";
    for (const auto& p : best) std::cout << p.x << " " << p.y << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
