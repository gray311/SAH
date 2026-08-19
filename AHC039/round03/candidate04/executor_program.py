# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Point { int x, y; };
struct Fish { Point p; int type; };
vector<Fish> all_fish;
vector<Point> poly;

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    all_fish.reserve(2 * N);
    for (int i = 0; i < N; i++) {
        int x, y; cin >> x >> y;
        all_fish.push_back({{x, y}, 1});
    }
    for (int i = 0; i < N; i++) {
        int x, y; cin >> x >> y;
        all_fish.push_back({{x, y}, -1});
    }
    
    // Simple approach: find bounding box of all mackerels
    int min_x = 200000, max_x = -200000, min_y = 200000, max_y = -200000;
    for (auto& f : all_fish) {
        if (f.type == 1) {
            min_x = min(min_x, f.p.x);
            max_x = max(max_x, f.p.x);
            min_y = min(min_y, f.p.y);
            max_y = max(max_y, f.p.y);
        }
    }
    
    if (min_x > max_x || min_y > max_y) {
        poly = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
    } else {
        poly = {{min_x, min_y}, {max_x, min_y}, {max_x, max_y}, {min_x, max_y}};
    }
    
    cout << poly.size() << "\n";
    for (auto& p : poly) {
        cout << p.x << " " << p.y << "\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
