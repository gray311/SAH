# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <bits/stdc++.h>
using namespace std;

const int MAX_COORD = 100000;

struct Point { int x, y; };
struct Fish { Point p; int type; };
vector<Fish> fish;

int score_polygon(const vector<Point>& poly) {
    if(poly.size() < 4) return 0;
    int m=0, s=0;
    for(const auto& f : fish) {
        bool inside = false;
        for(size_t i=0; i<poly.size(); ++i) {
            Point p1 = poly[i];
            Point p2 = poly[(i+1) % poly.size()];
            if(p1.y == p2.y) continue;
            bool cond = (p1.y > f.p.y) != (p2.y > f.p.y);
            double xint = (double)(p2.x - p1.x) * (f.p.y - p1.y) / (p2.y - p1.y) + p1.x;
            if(cond && f.p.x < xint) inside = !inside;
        }
        if(inside) {
            if(f.type == 1) m++;
            else s++;
        }
    }
    return m - s;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    srand(42);
    
    int n;
    cin >> n;
    fish.resize(2*n);
    
    for(int i=0; i<n; ++i) {
        cin >> fish[i].p.x >> fish[i].p.y;
        fish[i].type = 1;
    }
    for(int i=0; i<n; ++i) {
        cin >> fish[n+i].p.x >> fish[n+i].p.y;
        fish[n+i].type = -1;
    }
    
    vector<Point> best_poly;
    int best_score = 0;
    
    // Random polygons with hill climbing
    for(int restart=0; restart<10; ++restart) {
        vector<Point> poly;
        poly.reserve(6);
        for(int i=0; i<6; ++i) {
            poly.push_back({(rand() % 30001) * 3, (rand() % 30001) * 3});
        }
        
        for(int iter=0; iter<4; ++iter) {
            int best_iter_score = score_polygon(poly);
            
            for(int i=0; i<poly.size(); ++i) {
                for(int dx=-15; dx<=15; dx+=5) {
                    for(int dy=-15; dy<=15; dy+=5) {
                        if(dx==0 && dy==0) continue;
                        poly[i].x += dx;
                        poly[i].y += dy;
                        poly[i].x = max(0, min(MAX_COORD, poly[i].x));
                        poly[i].y = max(0, min(MAX_COORD, poly[i].y));
                        
                        int score = score_polygon(poly);
                        if(score > best_iter_score) {
                            best_iter_score = score;
                        } else {
                            poly[i].x -= dx;
                            poly[i].y -= dy;
                        }
                    }
                }
            }
        }
        
        int score = score_polygon(poly);
        if(score > best_score) {
            best_score = score;
            best_poly = poly;
        }
    }
    
    // Large random rectangles
    for(int i=0; i<40; ++i) {
        Point p1 = {(rand() % 80001), (rand() % 80001)};
        int w = 25000 + (rand() % 25000);
        int h = 25000 + (rand() % 25000);
        Point p2 = {min(p1.x + w, MAX_COORD), min(p1.y + h, MAX_COORD)};
        
        vector<Point> poly = {{p1.x, p1.y}, {p2.x, p1.y}, {p2.x, p2.y}, {p1.x, p2.y}};
        int score = score_polygon(poly);
        if(score > best_score) {
            best_score = score;
            best_poly = poly;
        }
    }
    
    // Grid-aligned rectangles
    for(int base=0; base<25; ++base) {
        for(int sz=20000; sz<=40000; sz+=5000) {
            Point p1 = {(base * 4000), (base * 4000)};
            Point p2 = {min(p1.x + sz, MAX_COORD), min(p1.y + sz, MAX_COORD)};
            
            vector<Point> poly = {{p1.x, p1.y}, {p2.x, p1.y}, {p2.x, p2.y}, {p1.x, p2.y}};
            int score = score_polygon(poly);
            if(score > best_score) {
                best_score = score;
                best_poly = poly;
            }
        }
    }
    
    // More rectangle sizes
    for(int base=0; base<20; ++base) {
        for(int sz=15000; sz<=45000; sz+=4000) {
            Point p1 = {(base * 3500), (base * 3500)};
            Point p2 = {min(p1.x + sz, MAX_COORD), min(p1.y + sz, MAX_COORD)};
            
            vector<Point> poly = {{p1.x, p1.y}, {p2.x, p1.y}, {p2.x, p2.y}, {p1.x, p2.y}};
            int score = score_polygon(poly);
            if(score > best_score) {
                best_score = score;
                best_poly = poly;
            }
        }
    }
    
    // Asymmetric rectangles
    for(int i=0; i<25; ++i) {
        Point p1 = {(rand() % 100001), (rand() % 100001)};
        int w = 20000 + (rand() % 30000);
        int h = 25000 + (rand() % 25000);
        Point p2 = {min(p1.x + w, MAX_COORD), min(p1.y + h, MAX_COORD)};
        
        vector<Point> poly = {{p1.x, p1.y}, {p2.x, p1.y}, {p2.x, p2.y}, {p1.x, p2.y}};
        int score = score_polygon(poly);
        if(score > best_score) {
            best_score = score;
            best_poly = poly;
        }
    }
    
    cout << best_poly.size() << "\n";
    for(const auto& p : best_poly) {
        cout << p.x << " " << p.y << "\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
