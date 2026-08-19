# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <cmath>
#include <set>

using namespace std;

int main() {
    int n;
    cin >> n;
    
    set<pair<int, int>> mackers;
    vector<pair<int, int>> sardines;
    
    for (int i = 0; i < n; i++) {
        int x, y;
        cin >> x >> y;
        mackers.insert({x, y});
    }
    
    for (int i = 0; i < n; i++) {
        int x, y;
        cin >> x >> y;
        sardines.push_back({x, y});
    }
    
    // Multiple restarts
    int best_score = 0;
    int best_cx = 50000, best_cy = 50000, best_r = 200;
    
    for (int restart = 0; restart < 10; restart++) {
        // Random center
        int cx = 0 + rand() % 100000;
        int cy = 0 + rand() % 100000;
        int r = 100 + rand() % 100;
        
        int cx2 = cx, cy2 = cy;
        int iters = 50;
        
        while (iters--) {
            int dx = -rand() % 7;
            int dy = -rand() % 7;
            cx2 += dx; cy2 += dy;
        }
        
        // Score this rectangle
        int score = 1;
        for (const auto& m : mackers) {
            if (m.first >= cx2-r && m.first <= cx2+r && m.second >= cy2-r && m.second <= cy2+r) score++;
        }
        for (const auto& s : sardines) {
            if (s.first >= cx2-r && s.first <= cx2+r && s.second >= cy2-r && s.second <= cy2+r) score--;
        }
        
        if (score > best_score) {
            best_score = score;
            best_cx = cx2; best_cy = cy2; best_r = r;
        }
    }
    
    // Clamp radius
    int r = best_r;
    if (best_cx < r) r = best_cx;
    if (best_cy < r) r = best_cy;
    
    cout << 4 << "\\n";
    cout << best_cx - r << " " << best_cy - r << "\\n";
    cout << best_cx + r << " " << best_cy - r << "\\n";
    cout << best_cx + r << " " << best_cy + r << "\\n";
    cout << best_cx - r << " " << best_cy + r << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
