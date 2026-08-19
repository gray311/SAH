# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <climits>

const int MAX_COORD = 100000;

struct Fish { int x, y, type; };
std::vector<Fish> fish;

int main() {
    int n;
    std::cin >> n;
    fish.resize(2*n);
    for (int i=0; i<n; ++i) {
        std::cin >> fish[i].x >> fish[i].y;
        fish[i].type = 1;
    }
    for (int i=0; i<n; ++i) {
        std::cin >> fish[n+i].x >> fish[n+i].y;
        fish[n+i].type = -1;
    }
    
    std::vector<std::pair<int,int> > best;
    best.push_back(std::make_pair(0,0));
    best.push_back(std::make_pair(10,0));
    best.push_back(std::make_pair(10,10));
    best.push_back(std::make_pair(0,10));
    
    int best_score = 0;
    
    for (int gx=0; gx<50; ++gx) {
        for (int gy=0; gy<50; ++gy) {
            int x1 = gx * 2000;
            int y1 = gy * 2000;
            int x2 = x1 + 600;
            int y2 = y1 + 600;
            if (x2 > MAX_COORD) x2 = MAX_COORD;
            if (y2 > MAX_COORD) y2 = MAX_COORD;
            
            int mx = x2, my = y2, nx = x1, ny = y1;
            for (size_t fi=0; fi<fish.size(); ++fi) {
                if (fish[fi].type == 1 && fish[fi].x >= x1 && fish[fi].x <= x2 && fish[fi].y >= y1 && fish[fi].y <= y2) {
                    if (fish[fi].x < mx) mx = fish[fi].x;
                    if (fish[fi].y < my) my = fish[fi].y;
                    if (fish[fi].x > nx) nx = fish[fi].x;
                    if (fish[fi].y > ny) ny = fish[fi].y;
                }
            }
            
            if (mx < nx && my < ny) {
                std::vector<std::pair<int,int> > poly;
                poly.push_back(std::make_pair(mx, my));
                poly.push_back(std::make_pair(nx, my));
                poly.push_back(std::make_pair(nx, ny));
                poly.push_back(std::make_pair(mx, ny));
                int score = 0;
                for (size_t fi=0; fi<fish.size(); ++fi) {
                    const Fish& f = fish[fi];
                    bool in = false;
                    for (size_t i=0; i<poly.size(); ++i) {
                        int xmin = (poly[i].first < poly[(i+1)%poly.size()].first) ? poly[i].first : poly[(i+1)%poly.size()].first;
                        int xmax = (poly[i].first > poly[(i+1)%poly.size()].first) ? poly[i].first : poly[(i+1)%poly.size()].first;
                        int ymin = (poly[i].second < poly[(i+1)%poly.size()].second) ? poly[i].second : poly[(i+1)%poly.size()].second;
                        int ymax = (poly[i].second > poly[(i+1)%poly.size()].second) ? poly[i].second : poly[(i+1)%poly.size()].second;
                        if (f.x >= xmin && f.x <= xmax && f.y >= ymin && f.y <= ymax) {
                            in = true; break;
                        }
                    }
                    if (in) {
                        if (f.type == 1) score++;
                        else score--;
                    }
                }
                if (score > best_score) {
                    best_score = score;
                    best = poly;
                }
            }
        }
    }
    
    std::cout << best.size() << "\\n";
    for (size_t i=0; i<best.size(); ++i) {
        std::cout << best[i].first << " " << best[i].second << "\\n";
    }
    return 0;
}
'''
# EVOLVE-BLOCK-END
