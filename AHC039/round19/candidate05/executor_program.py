# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAX_COORD = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct Point {
    int x, y;
};

vector<Point> mackerels;
vector<Point> sardines;

int count_fish_inside(const vector<Point>& poly, int fish_type) {
    if (poly.size() < 4) return 0;
    int count = 0;
    const vector<Point>& fish_list = (fish_type == 1) ? mackerels : sardines;
    
    for (size_t i = 0; i < fish_list.size(); ++i) {
        int x = fish_list[i].x;
        int y = fish_list[i].y;
        bool inside = false;
        for (int j = 0, k = (int)poly.size() - 1; j < (int)poly.size(); k = j++) {
            bool cond1 = (poly[j].y > y);
            bool cond2 = (poly[k].y > y);
            if (cond1 != cond2) {
                long long t = (long long)(poly[k].x - poly[j].x) * (y - poly[j].y);
                if (t < (long long)(poly[k].y - poly[j].y) * (poly[j].x - x + 1)) {
                    inside = !inside;
                }
            }
        }
        if (inside) count++;
    }
    return count;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int N;
    if (!(cin >> N)) return 0;
    
    mackerels.reserve(N);
    sardines.reserve(N);
    
    for (int i = 0; i < N; ++i) {
        int x, y;
        cin >> x >> y;
        mackerels.push_back({x, y});
    }
    
    for (int i = 0; i < N; ++i) {
        int x, y;
        cin >> x >> y;
        sardines.push_back({x, y});
    }
    
    if (mackerels.empty()) {
        cout << 4 << "\\n0 0\\n1 0\\n1 1\\n0 1\\n";
        return 0;
    }
    
    Point min_p = mackerels[0], max_p = mackerels[0];
    for (const auto& m : mackerels) {
        min_p.x = min(min_p.x, m.x); min_p.y = min(min_p.y, m.y);
        max_p.x = max(max_p.x, m.x); max_p.y = max(max_p.y, m.y);
    }
    
    vector<Point> poly;
    if (min_p.x != max_p.x && min_p.y != max_p.y) {
        poly.push_back({min_p.x, min_p.y});
        poly.push_back({max_p.x, min_p.y});
        poly.push_back({max_p.x, max_p.y});
        poly.push_back({min_p.x, max_p.y});
    } else {
        poly = {{min_p.x, min_p.y}, {min_p.x + 1, min_p.y}, {min_p.x + 1, min_p.y + 1}, {min_p.x, min_p.y + 1}};
    }
    
    cout << poly.size() << "\\n";
    for (const auto& p : poly) {
        cout << p.x << " " << p.y << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
