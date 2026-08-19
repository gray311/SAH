# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct XorShift {
    uint64_t x;
    XorShift() : x(std::chrono::steady_clock::now().time_since_epoch().count() ^ ((uint64_t)std::random_device()() << 32) ^ std::random_device()()) {}
    uint64_t next() { x ^= x << 13; x ^= x >> 7; x ^= x << 17; return x; }
    int next_int(int n) { if (n <= 0) return 0; return next() % n; }
    int next_int(int a, int b) { if (a > b) return a; return a + next_int(b - a + 1); }
    double next_double() { return next() / (double)UINT64_MAX; }
};
XorShift rng;

struct Point {
    int x, y;
    bool operator<(const Point& other) const { if (x != other.x) return x < other.x; return y < other.y; }
    bool operator==(const Point& other) const { return x == other.x && y == other.y; }
};

struct Fish {
    Point p;
    int type;
};
vector<Fish> all_fish;

long long calc_perimeter(const vector<Point>& poly) {
    if (poly.size() < 2) return 0;
    long long p = 0;
    for (size_t i = 0; i < poly.size(); ++i) p += abs(poly[i].x - poly[(i+1)%poly.size()].x) + abs(poly[i].y - poly[(i+1)%poly.size()].y);
    return p;
}

bool is_on_segment(Point p, Point a, Point b) {
    long long cp = (long long)(b.x - a.x) * (p.y - a.y) - (long long)(b.y - a.y) * (p.x - a.x);
    if (cp != 0) return false;
    return min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) && min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}

bool is_inside(Point p, const vector<Point>& poly) {
    int n = poly.size(); if (n < 3) return false;
    for (int i = 0; i < n; ++i) if (is_on_segment(p, poly[i], poly[(i+1)%n])) return true;
    int wn = 0;
    for (int i = 0; i < n; ++i) {
        Point a = poly[i], b = poly[(i+1)%n];
        if (a.y <= p.y) { if (b.y > p.y && (long long)(b.x - a.x) * (p.y - a.y) - (long long)(b.y - a.y) * (p.x - a.x) > 0) wn++; }
        else { if (b.y <= p.y && (long long)(b.x - a.x) * (p.y - a.y) - (long long)(b.y - a.y) * (p.x - a.x) < 0) wn--; }
    }
    return wn != 0;
}

void calc_score(const vector<Point>& poly, int& m_cnt, int& s_cnt) {
    m_cnt = 0; s_cnt = 0; if (poly.size() < 3) return;
    for (const auto& f : all_fish) if (is_inside(f.p, poly)) { if (f.type == 1) m_cnt++; else s_cnt++; }
}

vector<Point> build_polygon_from_grid() {
    const int GRID_W = 200, GRID_H = 200;
    vector<vector<int>> grid(GRID_W, vector<int>(GRID_H, 0));
    for (const auto& f : all_fish) {
        int gx = f.p.x / (MAX_COORD_VAL / GRID_W), gy = f.p.y / (MAX_COORD_VAL / GRID_H);
        gx = min(gx, GRID_W - 1); gy = min(gy, GRID_H - 1);
        grid[gx][gy] += f.type;
    }
    int best_score = -1e9, best_x = 0, best_y = 0, best_w = 1, best_h = 1;
    for (int x = 0; x < GRID_W - 1; ++x) for (int y = 0; y < GRID_H - 1; ++y) {
        int score = grid[x][y] + grid[x+1][y] + grid[x][y+1] + grid[x+1][y+1];
        if (score > best_score) { best_score = score; best_x = x; best_y = y; best_w = 2; best_h = 2; }
    }
    int cell_w = MAX_COORD_VAL / GRID_W, cell_h = MAX_COORD_VAL / GRID_H;
    int x1 = best_x * cell_w, y1 = best_y * cell_h, x2 = (best_x + best_w) * cell_w, y2 = (best_y + best_h) * cell_h;
    return {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
}

int main() {
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    int N; cin >> N;
    all_fish.resize(2 * N);
    for (int i = 0; i < N; ++i) { cin >> all_fish[i].p.x >> all_fish[i].p.y; all_fish[i].type = 1; }
    for (int i = 0; i < N; ++i) { cin >> all_fish[N + i].p.x >> all_fish[N + i].p.y; all_fish[N + i].type = -1; }
    
    vector<Point> poly = build_polygon_from_grid();
    cout << poly.size() << "\\n";
    for (const auto& p : poly) cout << p.x << " " << p.y << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
