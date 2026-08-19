# EVOLVE-BLOCK-START
CPP_CODE = '''#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAX_C = 100000;
const int MAX_V = 1000;

struct Point { int x, y; };
struct Fish { Point p; int type; };

vector<Fish> fish;
vector<Point> mats;

int main() {
    int N;
    cin >> N;
    
    for (int i = 0; i < N; i++) {
        int x, y;
        cin >> x >> y;
        fish.push_back({{x, y}, 1});
        mats.push_back({x, y});
    }
    
    // Simple bounding box of all mackerels
    int lx = MAX_C, rx = 0, ly = MAX_C, ry = 0;
    for (const auto& m : mats) {
        lx = min(lx, m.x);
        rx = max(rx, m.x);
        ly = min(ly, m.y);
        ry = max(ry, m.y);
    }
    
    if (lx >= rx) rx = lx + 50;
    if (ly >= ry) ry = ly + 50;
    
    if (lx < 0) lx = 0;
    if (rx > MAX_C) rx = MAX_C;
    if (ly < 0) ly = 0;
    if (ry > MAX_C) ry = MAX_C;
    
    vector<Point> poly;
    poly.reserve(4);
    poly.push_back({lx, ly});
    poly.push_back({rx, ly});
    poly.push_back({rx, ry});
    poly.push_back({lx, ry});
    
    int m_cnt = 0, s_cnt = 0;
    int n = poly.size();
    for (const auto& f : fish) {
        bool inside = false;
        // Ray casting for point in polygon
        if (n >= 4) {
            int wn = 0;
            for (int i = 0, j = n - 1; i < n; j = i++) {
                if (((poly[i].y > f.p.y) != (poly[j].y > f.p.y)) &&
                    (f.p.x < ((double)(poly[j].x - poly[i].x) * (f.p.y - poly[i].y) / (poly[j].y - poly[i].y)) + poly[i].x)) {
                    wn++;
                }
            }
            inside = (wn > 0);
        }
        if (inside) {
            if (f.type == 1) m_cnt++;
            else s_cnt++;
        }
    }
    
    cout << poly.size() << endl;
    for (const auto& p : poly) {
        cout << p.x << " " << p.y << endl;
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
