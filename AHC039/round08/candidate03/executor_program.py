# EVOLVE-BLOCK-START
CPP_CODE = '''#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

struct Point { int x, y; };

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    if (!(std::cin >> N)) return 0;
    
    std::vector<Point> macs;
    macs.reserve(N);
    for(int i=0;i<N;i++) {
        Point pt;
        std::cin >> pt.x >> pt.y;
        macs.push_back(pt);
    }
    std::vector<Point> sards;
    sards.reserve(N);
    for(int i=0;i<N;i++) {
        Point pt;
        std::cin >> pt.x >> pt.y;
        sards.push_back(pt);
    }
    
    // Count fish in rectangle
    auto countRect = [&](int x1, int y1, int x2, int y2) -> std::pair<int,int> {
        int m=0, s=0;
        for(size_t i=0; i<macs.size(); i++) {
            if (macs[i].x >= x1 && macs[i].x <= x2 && macs[i].y >= y1 && macs[i].y <= y2) m++;
        }
        for(size_t i=0; i<sards.size(); i++) {
            if (sards[i].x >= x1 && sards[i].x <= x2 && sards[i].y >= y1 && sards[i].y <= y2) s++;
        }
        return {m,s};
    };
    
    int bestScore = 0;
    Point bestPoly[4] = {{0,0}, {50000,0}, {50000,50000}, {0,50000}};
    
    // Find bounding box of all mackerels
    int minmx = 100000, maxmx = 0, minmy = 100000, maxmy = 0;
    for(size_t i=0; i<macs.size(); i++) {
        minmx = std::min(minmx, macs[i].x);
        maxmx = std::max(maxmx, macs[i].x);
        minmy = std::min(minmy, macs[i].y);
        maxmy = std::max(maxmy, macs[i].y);
    }
    
    // Ensure minimum size
    if (maxmx - minmx < 1) maxmx = minmx + 1;
    if (maxmy - minmy < 1) maxmy = minmy + 1;
    
    // Try different rectangles to avoid sardines
    for(int r=0; r<10; r++) {
        int sx = minmx + (r % 10) * 100;
        int sy = minmy + (r / 10) * 100;
        int ex = std::min(maxmx + 100, 50000);
        int ey = std::min(maxmy + 100, 50000);
        
        auto rs = countRect(sx, sy, ex, ey);
        int sc = rs.first - rs.second + 1;
        
        if (sc > bestScore) {
            bestScore = sc;
            bestPoly[0] = {sx,sy};
            bestPoly[1] = {ex,sy};
            bestPoly[2] = {ex,ey};
            bestPoly[3] = {sx,ey};
        }
    }
    
    // Fine-tune by moving edges
    for(int dx=-50; dx<=50; dx+=25) {
        for(int dy=-50; dy<=50; dy+=25) {
            int sx2 = std::max(0, bestPoly[0].x + dx);
            int sy2 = std::max(0, bestPoly[0].y + dy);
            int ex2 = std::min(50000, bestPoly[1].x + dx);
            int ey2 = std::min(50000, bestPoly[2].y + dy);
            
            if (ex2 <= sx2 || ey2 <= sy2) continue;
            
            auto rs2 = countRect(sx2, sy2, ex2, ey2);
            int sc2 = rs2.first - rs2.second + 1;
            
            if (sc2 > bestScore) {
                bestScore = sc2;
                bestPoly[0] = {sx2,sy2};
                bestPoly[1] = {ex2,sy2};
                bestPoly[2] = {ex2,ey2};
                bestPoly[3] = {sx2,ey2};
            }
        }
    }
    
    std::cout << 4 << std::endl;
    std::cout << bestPoly[0].x << " " << bestPoly[0].y << std::endl;
    std::cout << bestPoly[1].x << " " << bestPoly[1].y << std::endl;
    std::cout << bestPoly[2].x << " " << bestPoly[2].y << std::endl;
    std::cout << bestPoly[3].x << " " << bestPoly[3].y << std::endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
