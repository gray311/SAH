# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>

struct Point {
    int x, y;
};

struct Fish {
    Point p;
    int type;
};

std::vector<Fish> fish;

bool point_inside(Point p, const std::vector<Point>& poly) {
    int wn = 0;
    int n = poly.size();
    for (int i = 0; i < n; i++) {
        Point p1 = poly[i];
        Point p2 = poly[(i + 1) % n];
        if (p1.y <= p.y && p2.y > p.y) {
            if ((long long)(p2.x - p1.x) * (p.y - p1.y) - (long long)(p2.y - p1.y) * (p.x - p1.x) > 0) {
                wn++;
            }
        } else if (p2.y <= p.y && p1.y > p.y) {
            if ((long long)(p2.x - p1.x) * (p.y - p1.y) - (long long)(p2.y - p1.y) * (p.x - p1.x) < 0) {
                wn--;
            }
        }
    }
    return wn != 0;
}

void compute_score(const std::vector<Point>& poly, int& m_cnt, int& s_cnt) {
    m_cnt = 0; s_cnt = 0;
    for (const auto& f : fish) {
        if (point_inside(f.p, poly)) {
            if (f.type == 1) m_cnt++;
            else s_cnt++;
        }
    }
}

std::vector<Point> make_rect(int x1, int y1, int x2, int y2) {
    if (x1 > x2 || y1 > y2) return {{0,0}, {1,0}, {1,1}, {0,1}};
    return {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
}

int main() {
    int N;
    std::cin >> N;
    
    fish.clear();
    fish.reserve(2 * N);
    
    std::vector<Point> mackerels, sardines;
    
    for (int i = 0; i < N; i++) {
        int x, y;
        std::cin >> x >> y;
        mackerels.push_back({x, y});
        fish.push_back({{x, y}, 1});
    }
    for (int i = 0; i < N; i++) {
        int x, y;
        std::cin >> x >> y;
        sardines.push_back({x, y});
        fish.push_back({{x, y}, -1});
    }
    
    std::vector<Point> best_poly = {{0,0}, {1,0}, {1,1}, {0,1}};
    int best_score = 0;
    
    // Compute score for bounding box of mackerels
    int minx = 100000, maxx = 0, miny = 100000, maxy = 0;
    for (const auto& p : mackerels) {
        minx = std::min(minx, p.x);
        maxx = std::max(maxx, p.x);
        miny = std::min(miny, p.y);
        maxy = std::max(maxy, p.y);
    }
    
    std::vector<Point> poly = make_rect(minx, miny, maxx, maxy);
    int m, s;
    compute_score(poly, m, s);
    int score = std::max(0, m - s + 1);
    if (score > best_score) {
        best_score = score;
        best_poly = poly;
    }
    
    // Try expanding the bounding box
    for (int dx = -1; dx <= 1; dx++) {
        for (int dy = -1; dy <= 1; dy++) {
            int nx = minx + dx, ny = miny + dy, nx2 = maxx + dx, ny2 = maxy + dy;
            poly = make_rect(nx, ny, nx2, ny2);
            compute_score(poly, m, s);
            score = std::max(0, m - s + 1);
            if (score > best_score) {
                best_score = score;
                best_poly = poly;
            }
        }
    }
    
    // Try horizontal strips - collect y coordinates
    std::set<int> y_unique;
    for (const auto& p : mackerels) {
        y_unique.insert(p.y);
    }
    
    // Sort y by mackerel count descending
    std::vector<int> sorted_ys(y_unique.begin(), y_unique.end());
    std::sort(sorted_ys.begin(), sorted_ys.end(), [&](int a, int b) {
        int ca = 0, cb = 0;
        for (const auto& p : mackerels) {
            if (p.y == a) ca++;
            if (p.y == b) cb++;
        }
        return ca > cb;
    });
    
    // Try top 20 y coordinates for horizontal strips
    for (size_t i = 0; i < std::min(sorted_ys.size(), size_t(20)); i++) {
        int y = sorted_ys[i];
        int min_x = 100000, max_x = 0;
        for (const auto& p : mackerels) {
            if (p.y == y) {
                min_x = std::min(min_x, p.x);
                max_x = std::max(max_x, p.x);
            }
        }
        if (min_x <= max_x) {
            poly = make_rect(min_x, y, max_x, y);
            compute_score(poly, m, s);
            score = std::max(0, m - s + 1);
            if (score > best_score) {
                best_score = score;
                best_poly = poly;
            }
        }
    }
    
    // Try vertical strips - collect x coordinates
    std::set<int> x_unique;
    for (const auto& p : mackerels) {
        x_unique.insert(p.x);
    }
    std::vector<int> sorted_xs(x_unique.begin(), x_unique.end());
    std::sort(sorted_xs.begin(), sorted_xs.end(), [&](int a, int b) {
        int ca = 0, cb = 0;
        for (const auto& p : mackerels) {
            if (p.x == a) ca++;
            if (p.x == b) cb++;
        }
        return ca > cb;
    });
    
    // Try top 20 x coordinates for vertical strips
    for (size_t i = 0; i < std::min(sorted_xs.size(), size_t(20)); i++) {
        int x = sorted_xs[i];
        int min_y = 100000, max_y = 0;
        for (const auto& p : mackerels) {
            if (p.x == x) {
                min_y = std::min(min_y, p.y);
                max_y = std::max(max_y, p.y);
            }
        }
        if (min_y <= max_y) {
            poly = make_rect(x, min_y, x, max_y);
            compute_score(poly, m, s);
            score = std::max(0, m - s + 1);
            if (score > best_score) {
                best_score = score;
                best_poly = poly;
            }
        }
    }
    
    // Try combining adjacent y coordinates into rectangles (limited)
    for (size_t i = 0; i < sorted_ys.size(); i++) {
        int y1 = sorted_ys[i];
        for (size_t j = i; j < std::min(sorted_ys.size(), size_t(i + 5)); j++) {
            int y2 = sorted_ys[j];
            int x_min = 100000, x_max = 0;
            
            for (const auto& p : mackerels) {
                if (p.y >= y1 && p.y <= y2) {
                    x_min = std::min(x_min, p.x);
                    x_max = std::max(x_max, p.x);
                }
            }
            
            if (x_min <= x_max) {
                poly = make_rect(x_min, y1, x_max, y2);
                compute_score(poly, m, s);
                score = std::max(0, m - s + 1);
                if (score > best_score) {
                    best_score = score;
                    best_poly = poly;
                }
            }
        }
    }
    
    // Output best polygon
    std::cout << best_poly.size() << "\\n";
    for (const auto& p : best_poly) {
        std::cout << p.x << " " << p.y << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
