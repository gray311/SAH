# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <set>
#include <cmath>
#include <numeric>

const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct Point {
    int x, y;
    bool operator<(const Point& o) const { return x != o.x ? x < o.x : y < o.y; }
    bool operator==(const Point& o) const { return x == o.x && y == o.y; }
};

struct Fish {
    Point p; int type;
};
std::vector<Fish> all_fish;

long long perim(const std::vector<Point>& p) {
    if (p.size() < 2) return 0;
    long long t = 0;
    for (size_t i = 0; i < p.size(); ++i)
        t += std::abs(p[i].x - p[(i+1)%p.size()].x) + std::abs(p[i].y - p[(i+1)%p.size()].y);
    return t;
}

bool inside(Point p, const std::vector<Point>& poly) {
    int wn = 0, n = poly.size();
    if (n < 3) return false;
    for (int i = 0; i < n; ++i) {
        Point a = poly[i], b = poly[(i+1)%n];
        if (a.y <= p.y && b.y > p.y) {
            if (p.x < b.x + (double)(b.x-a.x)*(p.y-a.y)/(b.y-a.y)) wn++;
        } else if (b.y <= p.y && a.y > p.y) {
            if (p.x < a.x + (double)(a.x-b.x)*(p.y-b.y)/(a.y-b.y)) wn--;
        }
    }
    return wn != 0;
}

bool valid_poly(const std::vector<Point>& poly) {
    if (poly.size() < 4 || poly.size() > MAX_VERTICES) return false;
    if (perim(poly) > MAX_PERIMETER) return false;
    std::set<Point> pts;
    for (const auto& p : poly) if (!pts.insert(p).second) return false;
    for (size_t i = 0; i < poly.size(); ++i) {
        Point a = poly[i], b = poly[(i+1)%poly.size()];
        if (a.x == b.x && a.y == b.y) return false;
        if (a.x != b.x && a.y != b.y) return false;
    }
    return true;
}

int N;

int evaluate(const std::vector<Point>& poly) {
    int m_cnt = 0, s_cnt = 0;
    for (const auto& f : all_fish) {
        int wn = 0, n = poly.size();
        if (n < 3) continue;
        for (int k = 0; k < n; ++k) {
            Point a = poly[k], b = poly[(k+1)%n];
            if (a.y <= f.p.y && b.y > f.p.y) {
                if (f.p.x < b.x + (double)(b.x-a.x)*(f.p.y-a.y)/(b.y-a.y)) wn++;
            } else if (b.y <= f.p.y && a.y > f.p.y) {
                if (f.p.x < a.x + (double)(a.x-b.x)*(f.p.y-b.y)/(a.y-b.y)) wn--;
            }
        }
        if (wn != 0) { if (f.type == 1) m_cnt++; else s_cnt++; }
    }
    return m_cnt - s_cnt + 1;
}

int best_global_score = 0;
std::vector<Point> best_global_poly;

int evaluate_and_update(const std::vector<Point>& poly) {
    int score = evaluate(poly);
    if (score > best_global_score) {
        best_global_score = score;
        best_global_poly = poly;
    }
    return score;
}

void solve() {
    all_fish.resize(2 * N);
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[i].p.x >> all_fish[i].p.y;
        all_fish[i].type = 1;
    }
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[N+i].p.x >> all_fish[N+i].p.y;
        all_fish[N+i].type = -1;
    }
    
    if (all_fish.empty()) {
        std::cout << "4" << "\n" << "0 0" << "\n" << "1 0" << "\n" << "1 1" << "\n" << "0 1" << "\n";
        return;
    }
    
    int best_score = 0;
    std::vector<Point> best_poly;
    
    // Try different clustering radii
    int radii[] = {1000, 1500, 2000, 2500, 3000};
    for (int radius : radii) {
        std::vector<std::vector<Point>> clusters;
        std::vector<bool> visited(2*N, false);
        
        for (int i = 0; i < 2*N; ++i) {
            if (all_fish[i].type != 1 || visited[i]) continue;
            std::vector<Point> cluster;
            std::vector<int> q;
            q.reserve(2*N);
            q.push_back(i);
            visited[i] = true;
            int head = 0;
            while (head < (int)q.size()) {
                int cur = q[head++];
                cluster.push_back(all_fish[cur].p);
                for (int j = 0; j < 2*N; ++j) {
                    if (!visited[j] && all_fish[j].type == 1) {
                        long long dx = all_fish[j].p.x - all_fish[cur].p.x;
                        long long dy = all_fish[j].p.y - all_fish[cur].p.y;
                        if (dx*dx + dy*dy <= (long long)radius * radius) {
                            visited[j] = true;
                            q.push_back(j);
                        }
                    }
                }
            }
            if (cluster.size() > 0) clusters.push_back(cluster);
        }
        
        for (const auto& cluster : clusters) {
            int xmin = MAX_COORD_VAL, xmax = 0, ymin = MAX_COORD_VAL, ymax = 0;
            for (const auto& p : cluster) {
                xmin = std::min(xmin, p.x); xmax = std::max(xmax, p.x);
                ymin = std::min(ymin, p.y); ymax = std::max(ymax, p.y);
            }
            if (xmin > xmax || ymin > ymax) continue;
            
            std::vector<Point> poly = {{xmin,ymin}, {xmax,ymin}, {xmax,ymax}, {xmin,ymax}};
            if (valid_poly(poly)) {
                int score = evaluate(poly);
                if (score > best_score) {
                    best_score = score;
                    best_poly = poly;
                }
            }
        }
    }
    
    // Also try simple rectangle around all mackerels
    std::vector<Point> mackerel_coords;
    for (const auto& f : all_fish) if (f.type == 1) mackerel_coords.push_back(f.p);
    
    if (!mackerel_coords.empty()) {
        int mx = MAX_COORD_VAL, my = MAX_COORD_VAL, minx = MAX_COORD_VAL, miny = MAX_COORD_VAL;
        for (const auto& p : mackerel_coords) {
            mx = std::max(mx, p.x); my = std::max(my, p.y);
            minx = std::min(minx, p.x); miny = std::min(miny, p.y);
        }
        if (mx != minx || my != miny) {
            std::vector<Point> poly = {{minx,miny}, {mx,miny}, {mx,my}, {minx,my}};
            if (valid_poly(poly)) {
                int score = evaluate(poly);
                if (score > best_score) {
                    best_score = score;
                    best_poly = poly;
                }
            }
        }
    }
    
    // Try expanding the best polygon by 50 units in all directions
    if (best_score > 0 && best_poly.size() == 4) {
        int xmin = best_poly[0].x, xmax = best_poly[1].x, ymin = best_poly[0].y, ymax = best_poly[1].y;
        int best_exp_score = best_score;
        std::vector<Point> best_exp_poly = best_poly;
        
        for (int dx : {-50, 50}) {
            for (int dy : {-50, 50}) {
                int nxmin = xmin + dx, nxmax = xmax + dx, nymin = ymin + dy, nyymax = ymax + dy;
                if (nxmin < 0 || nxmax > MAX_COORD_VAL || nymin < 0 || nyymax > MAX_COORD_VAL) continue;
                if (nxmin > nxmax || nymin > nyymax) continue;
                
                std::vector<Point> new_poly = {{nxmin,nymin}, {nxmax,nymin}, {nxmax,nyymax}, {nxmin,nyymax}};
                if (valid_poly(new_poly)) {
                    int score = evaluate(new_poly);
                    if (score > best_exp_score) {
                        best_exp_score = score;
                        best_exp_poly = new_poly;
                    }
                }
            }
        }
        
        if (best_exp_score > best_score) {
            best_score = best_exp_score;
            best_poly = best_exp_poly;
        }
    }
    
    if (best_score <= 0) {
        std::cout << "4" << "\n" << "0 0" << "\n" << "1 0" << "\n" << "1 1" << "\n" << "0 1" << "\n";
    } else {
        std::cout << best_poly.size() << "\n";
        for (const auto& p : best_poly) std::cout << p.x << " " << p.y << "\n";
    }
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    try {
        std::cin >> N;
        if (N <= 0) N = 1;
        solve();
    } catch (...) {
        std::cout << "4" << "\n" << "0 0" << "\n" << "1 0" << "\n" << "1 1" << "\n" << "0 1" << "\n";
    }
    return 0;
}
'''
# EVOLVE-BLOCK-END
