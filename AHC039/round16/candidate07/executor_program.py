# EVOLVE-BLOCK-START
"""
# Simple mackerel-focused rectangle
"""

code = r'''#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <random>
#include <utility>

using namespace std;

const int NMAX = 100000, NV = 1000, PM = 400000;

struct Point { int i, j; };
static vector<Point> mackerels, sardines;

bool is_inside(const Point& p, const vector<Point>& poly) {
    int wn = 0, n = poly.size();
    for (int i = 0; i < n; ++i) {
        Point a = poly[i], b = poly[(i+1)%n];
        if (a.j <= p.j) {
            if (b.j > p.j && (long long)(b.i - a.i) * (p.j - a.j) - (long long)(b.j - a.j) * (p.i - a.i) > 0) wn++;
        } else {
            if (b.j <= p.j && (long long)(b.i - a.i) * (p.j - a.j) - (long long)(b.j - a.j) * (p.i - a.i) < 0) wn--;
        }
    }
    return wn != 0;
}

int evaluate_poly(const vector<Point>& poly) {
    if (poly.size() < 4) return 0;
    int m_cnt = 0, s_cnt = 0;
    for (const auto& f : mackerels) {
        if (is_inside(f, poly)) m_cnt++;
    }
    for (const auto& f : sardines) {
        if (is_inside(f, poly)) s_cnt++;
    }
    return max(0, m_cnt - s_cnt + 1);
}

long long perimeter(const vector<Point>& poly) {
    long long p = 0;
    for (size_t i = 0; i < poly.size(); ++i) {
        p += abs(poly[i].i - poly[(i+1)%poly.size()].i) + abs(poly[i].j - poly[(i+1)%poly.size()].j);
    }
    return p;
}

bool valid_poly(const vector<Point>& poly) {
    if (poly.size() < 4 || poly.size() > NV) return false;
    if (perimeter(poly) > PM) return false;
    for (const auto& p : poly) {
        if (p.i < 0 || p.i > NMAX || p.j < 0 || p.j > NMAX) return false;
    }
    return true;
}

bool check_self_intersection(const vector<Point>& poly) {
    int n = poly.size();
    if (n < 4) return false;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 2; j < n; ++j) {
            if (i == 0 && j == n-1) continue;
            long long c1 = (long long)(poly[(i+1)%n].i - poly[i].i) * (poly[j].j - poly[i].j) - 
                          (long long)(poly[(i+1)%n].j - poly[i].j) * (poly[j].i - poly[i].i);
            long long c2 = (long long)(poly[(j+1)%n].i - poly[j].i) * (poly[i].j - poly[j].j) - 
                          (long long)(poly[(j+1)%n].j - poly[j].j) * (poly[i].i - poly[j].i);
            if (c1 == 0 && c2 == 0) {
                int mn1 = min(poly[i].i, poly[(i+1)%n].i), mx1 = max(poly[i].i, poly[(i+1)%n].i);
                int mn2 = min(poly[j].i, poly[(j+1)%n].i), mx2 = max(poly[j].i, poly[(j+1)%n].i);
                int mnj1 = min(poly[i].j, poly[(i+1)%n].j), mj1 = max(poly[i].j, poly[(i+1)%n].j);
                int mnj2 = min(poly[j].j, poly[(j+1)%n].j), mj2 = max(poly[j].j, poly[(j+1)%n].j);
                if ((poly[i].i == poly[(i+1)%n].i && poly[j].i == poly[(j+1)%n].i) ||
                    (poly[i].j == poly[(i+1)%n].j && poly[j].j == poly[(j+1)%n].j)) {
                    if (max(mn1, mn2) <= min(mx1, mx2) && max(mnj1, mnj2) <= min(mj1, mj2))
                        return true;
                }
            } else if ((c1 > 0 && c2 > 0) || (c1 < 0 && c2 < 0)) continue;
            else return true;
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    if (!(cin >> N)) return 0;
    mackerels.reserve(N);
    sardines.reserve(N);
    
    for (int i = 0; i < N; ++i) {
        Point p;
        cin >> p.i >> p.j;
        mackerels.push_back(p);
    }
    for (int i = 0; i < N; ++i) {
        Point p;
        cin >> p.i >> p.j;
        sardines.push_back(p);
    }
    
    // Find bounding box of mackerels
    int min_x = NMAX, max_x = 0, min_y = NMAX, max_y = 0;
    for (const auto& f : mackerels) {
        min_x = min(min_x, f.i);
        max_x = max(max_x, f.i);
        min_y = min(min_y, f.j);
        max_y = max(max_y, f.j);
    }
    
    // Create a simple rectangle around mackerels
    vector<Point> poly = {{min_x, min_y}, {max_x + 1, min_y}, {max_x + 1, max_y}, {min_x, max_y}};
    
    // Hill climb: try shifting edges
    int shifts[] = {5, 10, 15, 20, 25};
    for (int r = 0; r < 3; ++r) {
        int best_score = evaluate_poly(poly);
        for (int dir = 0; dir < 4; ++dir) {
            Point p = poly[dir];
            Point q = poly[(dir + 1) % 4];
            
            for (int shift : shifts) {
                for (int sgn = -1; sgn <= 1; sgn += 2) {
                    vector<Point> test = poly;
                    if (dir == 0) { // Top edge - shift y
                        test[dir] = {p.i, p.j + sgn * shift};
                        test[(dir + 1) % 4] = {q.i, q.j + sgn * shift};
                    } else if (dir == 1) { // Right edge - shift x
                        test[dir] = {p.i + sgn * shift, p.j};
                        test[(dir + 1) % 4] = {q.i + sgn * shift, q.j};
                    } else if (dir == 2) { // Bottom edge - shift y
                        test[dir] = {p.i, p.j - sgn * shift};
                        test[(dir + 1) % 4] = {q.i, q.j - sgn * shift};
                    } else if (dir == 3) { // Left edge - shift x
                        test[dir] = {p.i - sgn * shift, p.j};
                        test[(dir + 1) % 4] = {q.i - sgn * shift, q.j};
                    }
                    
                    int sc = evaluate_poly(test);
                    if (sc > best_score) {
                        best_score = sc;
                        poly = test;
                    }
                }
            }
        }
    }
    
    if (!valid_poly(poly)) {
        poly = {{0, 0}, {NMAX, 0}, {NMAX, NMAX}, {0, NMAX}};
    }
    
    cout << poly.size() << "\n";
    for (const auto& p : poly) {
        cout << p.i << " " << p.j << "\n";
    }
    
    return 0;
}
'''

CPP_CODE = code
# EVOLVE-BLOCK-END
