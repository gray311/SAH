# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <numeric>

const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct Point {
    int x, y;
    bool operator<(const Point& other) const { return x != other.x ? x < other.x : y < other.y; }
    bool operator==(const Point& other) const { return x == other.x && y == other.y; }
};

struct Fish {
    Point p;
    int type;
};

std::vector<Fish> all_fish;

long long poly_perimeter(const std::vector<Point>& poly) {
    if (poly.size() < 2) return 0;
    long long p = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        p += std::abs(poly[i].x - poly[(i+1)%poly.size()].x) + std::abs(poly[i].y - poly[(i+1)%poly.size()].y);
    }
    return p;
}

bool is_inside(Point p, const std::vector<Point>& poly) {
    if (poly.size() < 3) return false;
    int wn = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        Point a = poly[i], b = poly[(i+1)%poly.size()];
        if (a.y <= p.y) {
            if (b.y > p.y && (long long)(b.x-a.x)*(p.y-a.y) > (long long)(b.y-a.y)*(p.x-a.x)) wn++;
        } else {
            if (b.y <= p.y && (long long)(b.x-a.x)*(p.y-a.y) < (long long)(b.y-a.y)*(p.x-a.x)) wn--;
        }
    }
    return wn != 0;
}

void calc_score(const std::vector<Point>& poly, int& m, int& s) {
    m = 0; s = 0;
    if (poly.size() < 3) return;
    for (const auto& f : all_fish) {
        if (is_inside(f.p, poly)) {
            if (f.type == 1) m++;
            else s++;
        }
    }
}

bool is_valid(const std::vector<Point>& poly) {
    int n = poly.size();
    if (n < 4 || n > MAX_VERTICES) return false;
    if (poly_perimeter(poly) > MAX_PERIMETER) return false;
    for (size_t i = 0; i < n; ++i) {
        if (poly[i].x < 0 || poly[i].x > MAX_COORD_VAL || poly[i].y < 0 || poly[i].y > MAX_COORD_VAL) return false;
        if (poly[i].x == poly[(i+1)%n].x && poly[i].y == poly[(i+1)%n].y) return false;
        if (poly[i].x != poly[(i+1)%n].x && poly[i].y != poly[(i+1)%n].y) return false;
    }
    std::set<Point> pts;
    for (const auto& p : poly) if (!pts.insert(p).second) return false;
    return true;
}

bool seg_intersect(Point a, Point b, Point c, Point d) {
    if (a.x == b.x && c.x == d.x) return std::max(a.y, b.y) <= std::min(c.y, d.y);
    if (a.y == b.y && c.y == d.y) return std::max(a.x, b.x) <= std::min(c.x, d.x);
    long long cp1 = (long long)(b.y-a.y)*(c.x-a.x) - (long long)(b.x-a.x)*(c.y-a.y);
    long long cp2 = (long long)(b.y-a.y)*(d.x-a.x) - (long long)(b.x-a.x)*(d.y-a.y);
    long long cp3 = (long long)(d.y-c.y)*(a.x-c.x) - (long long)(d.x-c.x)*(a.y-c.y);
    long long cp4 = (long long)(d.y-c.y)*(b.x-c.x) - (long long)(d.x-c.x)*(b.y-c.y);
    return ((cp1 > 0 && cp2 < 0) || (cp1 < 0 && cp2 > 0)) && ((cp3 > 0 && cp4 < 0) || (cp3 < 0 && cp4 > 0));
}

bool has_intersection(const std::vector<Point>& poly) {
    int n = poly.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 2; j < n; ++j) {
            if (i == 0 && j == n - 1) continue;
            if (seg_intersect(poly[i], poly[(i+1)%n], poly[j], poly[(j+1)%n])) return true;
        }
    }
    return false;
}

std::vector<Point> make_rect(int cx, int cy, int w, int h) {
    return {{cx-w, cy-h}, {cx+w, cy-h}, {cx+w, cy+h}, {cx-w, cy+h}};
}

void extend_edge(std::vector<Point>& poly, int idx, int dir, int dist) {
    int n = poly.size();
    Point p1 = poly[idx], p2 = poly[(idx+1)%n];
    if (p1.x == p2.x) {
        if (dir == 1) poly[idx].x = poly[(idx+1)%n].x = p2.x + dist;
        else poly[idx].x = poly[(idx+1)%n].x = p1.x - dist;
    } else {
        if (dir == 1) poly[idx].y = poly[(idx+1)%n].y = p2.y + dist;
        else poly[idx].y = poly[(idx+1)%n].y = p1.y - dist;
    }
}

std::vector<Point> evolve(const std::vector<Point>& init) {
    std::vector<Point> best = init;
    int bm = 0, bs = 0;
    calc_score(best, bm, bs);
    std::vector<Point> curr = best;
    int cm = bm, cs = bs;
    
    for (int iter = 0; iter < 8; ++iter) {
        std::vector<Point> nxt = curr;
        for (int i = 0; i < 4; ++i) {
            for (int d : {10, 20, 50, 100}) {
                std::vector<Point> t = nxt;
                extend_edge(t, i % t.size(), 1, d);
                if (!is_valid(t) || has_intersection(t)) continue;
                int tm = 0, ts = 0;
                calc_score(t, tm, ts);
                if (tm - ts > cm - cs) { cm = tm; cs = ts; curr = t; break; }
            }
            for (int d : {10, 20, 50, 100}) {
                std::vector<Point> t = nxt;
                extend_edge(t, i % t.size(), -1, d);
                if (!is_valid(t) || has_intersection(t)) continue;
                int tm = 0, ts = 0;
                calc_score(t, tm, ts);
                if (tm - ts > cm - cs) { cm = tm; cs = ts; curr = t; break; }
            }
        }
        for (const auto& f : all_fish) {
            if (f.type == -1 && is_inside(f.p, curr)) {
                for (int dx : {10, 20}) {
                    for (int dy : {10, 20}) {
                        std::vector<Point> t = curr;
                        t.insert(t.begin() + 1, {std::max(0, f.p.x - dx), f.p.y});
                        t.insert(t.begin() + 2, {std::min(20, f.p.x + dx), f.p.y});
                        if (!is_valid(t) || has_intersection(t)) continue;
                        int tm = 0, ts = 0;
                        calc_score(t, tm, ts);
                        if (tm - ts > cm - cs) { cm = tm; cs = ts; curr = t; }
                    }
                }
            }
        }
        for (size_t i = 0; i < curr.size(); ++i) {
            for (int dx : {-5, 5, -10, 10}) {
                for (int dy : {-5, 5, -10, 10}) {
                    if (dx == 0 && dy == 0) continue;
                    std::vector<Point> t = curr;
                    Point orig = t[i];
                    t[i] = {std::max(0, std::min(MAX_COORD_VAL, orig.x + dx)), std::max(0, std::min(MAX_COORD_VAL, orig.y + dy))};
                    if (!is_valid(t) || has_intersection(t)) continue;
                    int tm = 0, ts = 0;
                    calc_score(t, tm, ts);
                    if (tm - ts > cm - cs) { cm = tm; cs = ts; curr = t; }
                }
            }
        }
        if (curr.size() >= 4 && is_valid(curr) && !has_intersection(curr)) {
            int tm = 0, ts = 0;
            calc_score(curr, tm, ts);
            if (tm - ts > bm - bs) { bm = tm; bs = ts; best = curr; }
        }
    }
    return best;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int N;
    std::cin >> N;
    all_fish.resize(2 * N);
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[i].p.x >> all_fish[i].p.y;
        all_fish[i].type = 1;
    }
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[N+i].p.x >> all_fish[N+i].p.y;
        all_fish[N+i].type = -1;
    }
    
    std::vector<Point> best_poly;
    bool found = false;
    for (int r = 0; r < 8; ++r) {
        int mx = 100000, MM = 0, my = 100000, MM2 = 0;
        for (int i = 0; i < N; ++i) {
            mx = std::min(mx, all_fish[i].p.x);
            MM = std::max(MM, all_fish[i].p.x);
            my = std::min(my, all_fish[i].p.y);
            MM2 = std::max(MM2, all_fish[i].p.y);
        }
        int cx = (mx + MM) / 2, cy = (my + MM2) / 2;
        int w = std::max(5000, MM - mx + 1000);
        int h = std::max(5000, MM2 - my + 1000);
        std::vector<Point> init = make_rect(cx, cy, w/2, h/2);
        if (!is_valid(init) || has_intersection(init)) init = {{0, 0}, {10000, 0}, {10000, 10000}, {0, 10000}};
        std::vector<Point> poly = evolve(init);
        if (poly.size() < 4 || !is_valid(poly) || has_intersection(poly)) poly = {{0, 0}, {10000, 0}, {10000, 10000}, {0, 10000}};
        int pm = 0, ps = 0;
        calc_score(poly, pm, ps);
        if (pm - ps > 0) {
            if (pm - ps > best_poly.size()) { best_poly = poly; found = true; }
        }
    }
    if (!found) best_poly = {{0, 0}, {10000, 0}, {10000, 10000}, {0, 10000}};
    
    std::cout << best_poly.size() << "\\n";
    for (const auto& p : best_poly) std::cout << p.x << " " << p.y << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
