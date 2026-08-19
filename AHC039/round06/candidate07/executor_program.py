# EVOLVE-BLOCK-START
CPP_CODE = '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int n;
    cin >> n;
    
    vector<pair<int,int>> mackerels(n), sardines(n);
    for (int i = 0; i < n; i++) cin >> mackerels[i].first >> mackerels[i].second;
    for (int i = 0; i < n; i++) cin >> sardines[i].first >> sardines[i].second;
    
    auto count = [&](const pair<int,int>& x1, const pair<int,int>& x2) {
        int cm = 0, cs = 0;
        for (const auto& m : mackerels) {
            if (m.first >= x1.first && m.first <= x2.first && m.second >= x1.second && m.second <= x2.second) cm++;
        }
        for (const auto& s : sardines) {
            if (s.first >= x1.first && s.first <= x2.first && s.second >= x1.second && s.second <= x2.second) cs++;
        }
        return cm - cs;
    };
    
    int best_val = -1000000;
    vector<pair<int,int>> best_rect;
    
    // Many diverse random trials with varied sizes
    for (int trial = 0; trial < 3000; trial++) {
        int size_x = rand() % 35000 + 500;
        int size_y = rand() % 35000 + 500;
        int x1 = rand() % (100000 - size_x);
        int x2 = x1 + size_x;
        int y1 = rand() % (100000 - size_y);
        int y2 = y1 + size_y;
        
        int val = count({x1, y1}, {x2, y2});
        if (val > best_val) {
            best_val = val;
            best_rect = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
        }
    }
    
    srand(12345);
    for (int iter = 0; iter < 150000; iter++) {
        vector<pair<int,int>> cand = best_rect;
        int idx = rand() % 4;
        int step = rand() % 14 - 7;
        
        int nx = cand[idx].first + step;
        if (nx < 0 || nx > 100000) continue;
        else {
            cand[idx].first = nx;
            cand[(idx+1)%4].first = nx;
        }
        
        pair<int,int> p1 = cand[0], p2 = cand[1];
        int val = count(p1, p2);
        if (val > best_val) {
            best_rect = cand;
            best_val = val;
        }
    }
    
    cout << best_rect.size() << "\\n";
    for (const auto& p : best_rect) cout << p.first << " " << p.second << "\\n";
    
    return 0;
}'''
# EVOLVE-BLOCK-END
