# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <cstdlib>

using namespace std;

const int MAX_COORD = 100000;
const int MAX_PERIMETER = 400000;
const int MAX_VERTICES = 1000;

struct Point { int x, y; };
struct Fish { Point p; int type; };
vector<Fish> fish;
int N;

long long calc_perimeter(const vector<Point>& poly) {
    if (poly.size() < 2) return 0;
    long long p = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        const Point& a = poly[i];
        const Point& b = poly[(i + 1) % poly.size()];
        p += abs(a.x - b.x) + abs(a.y - b.y);
    }
    return p;
}

bool point_in_polygon(Point p, const vector<Point>& poly) {
    int wn = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        if (poly[i].y <= p.y) {
            if (poly[(i + 1) % poly.size()].y > p.y) {
                if ((long long)(poly[(i + 1) % poly.size()].x - poly[i].x) * (p.y - poly[i].y) > 0) wn++;
            }
        } else {
            if (poly[(i + 1) % poly.size()].y <= p.y) {
                if ((long long)(poly[(i + 1) % poly.size()].x - poly[i].x) * (p.y - poly[i].y) < 0) wn--;
            }
        }
    }
    return wn != 0;
}

bool valid_polygon(const vector<Point>& poly) {
    if (poly.size() < 4 || poly.size() > MAX_VERTICES) return false;
    for (size_t i = 0; i < poly.size(); ++i) {
        const Point& a = poly[i];
        const Point& b = poly[(i + 1) % poly.size()];
        if (a.x < 0 || a.x > MAX_COORD || a.y < 0 || a.y > MAX_COORD ||
            b.x < 0 || b.x > MAX_COORD || b.y < 0 || b.y > MAX_COORD) return false;
        if (a.x == b.x && a.y == b.y) return false;
        if (a.x != b.x && a.y != b.y) return false;
    }
    return calc_perimeter(poly) <= MAX_PERIMETER;
}

int main() {
    srand(42);
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N_in;
    cin >> N_in;
    N = N_in;
    fish.resize(2 * N_in);
    
    for (int i = 0; i < N_in; ++i) {
        cin >> fish[i].p.x >> fish[i].p.y;
        fish[i].type = 1;
    }
    for (int i = 0; i < N_in; ++i) {
        cin >> fish[N_in + i].p.x >> fish[N_in + i].p.y;
        fish[N_in + i].type = -1;
    }
    
    vector<int> clusters;
    if (N_in == 0) {
        cout << 4 << "\n0 0\n1 0\n1 1\n0 1\n";
        return 0;
    }
    
    vector<bool> visited(N_in, false);
    for (int i = 0; i < N_in; ++i) {
        if (visited[i]) continue;
        vector<int> cluster;
        vector<int> q;
        q.push_back(i);
        visited[i] = true;
        while (!q.empty()) {
            int u = q.back(); q.pop_back();
            cluster.push_back(u);
            for (int v = 0; v < N_in; ++v) {
                if (visited[v]) continue;
                if (abs(fish[u].p.x - fish[v].p.x) <= 5000 && 
                    abs(fish[u].p.y - fish[v].p.y) <= 5000) {
                    visited[v] = true;
                    q.push_back(v);
                }
            }
        }
        if (cluster.size() >= 1) clusters.push_back(cluster[0]);
        if (cluster.size() > 3) clusters.push_back(cluster[cluster.size() / 2]);
    }
    
    vector<Point> best_poly;
    int best_m = 0, best_s = 0;
    
    // Try many rectangles with various expansions and seeds
    for (int r = 0; r < 15; ++r) {
        int seed_idx = clusters[r % clusters.size()];
        int expand = 120 + rand() % 381; // 120-500
        
        Point c = fish[seed_idx].p;
        int x1 = max(0, c.x - expand);
        int x2 = min(MAX_COORD, c.x + expand);
        int y1 = max(0, c.y - expand);
        int y2 = min(MAX_COORD, c.y + expand);
        
        if (x1 >= x2 || y1 >= y2) continue;
        
        vector<Point> poly = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
        if (!valid_polygon(poly)) continue;
        
        int m = 0, s = 0;
        for (const auto& f : fish) {
            if (point_in_polygon(f.p, poly)) { if (f.type == 1) m++; else s++; }
        }
        
        if (m - s + 1 > best_m - best_s) {
            best_m = m; best_s = s;
            best_poly = poly;
        }
    }
    
    // Also try with first few mackerels directly
    for (int i = 0; i < min(5, (int)N_in); ++i) {
        int expand = 150 + rand() % 351;
        Point c = fish[i].p;
        int x1 = max(0, c.x - expand);
        int x2 = min(MAX_COORD, c.x + expand);
        int y1 = max(0, c.y - expand);
        int y2 = min(MAX_COORD, c.y + expand);
        
        if (x1 >= x2 || y1 >= y2) continue;
        
        vector<Point> poly = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
        if (!valid_polygon(poly)) continue;
        
        int m = 0, s = 0;
        for (const auto& f : fish) {
            if (point_in_polygon(f.p, poly)) { if (f.type == 1) m++; else s++; }
        }
        
        if (m - s + 1 > best_m - best_s) {
            best_m = m; best_s = s;
            best_poly = poly;
        }
    }
    
    // Fallback
    if (best_poly.empty() && N_in > 0) {
        Point c = fish[0].p;
        int exp = 200;
        int x1 = max(0, c.x - exp), x2 = min(MAX_COORD, c.x + exp);
        int y1 = max(0, c.y - exp), y2 = min(MAX_COORD, c.y + exp);
        if (x1 < x2 && y1 < y2) best_poly = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
    }
    if (best_poly.empty()) best_poly = {{0,0}, {1,0}, {1,1}, {0,1}};
    
    cout << best_poly.size() << "\n";
    for (const auto& p : best_poly) cout << p.x << " " << p.y << "\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
