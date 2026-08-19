# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>

using namespace std;
int main() {
    int N;
    cin >> N;
    vector<pair<int,int>> fish(2*N);
    for(int i=0;i<N;++i) cin >> fish[i].first >> fish[i].second;
    for(int i=0;i<N;++i) cin >> fish[N+i].first >> fish[N+i].second;
    
    auto start = chrono::steady_clock::now();
    mt19937 rng(42);
    
    vector<int> vx = {0, 500, 500, 0};
    vector<int> vy = {0, 0, 500, 500};
    
    for(int r=0;r<100;++r) {
        auto now = chrono::steady_clock::now();
        auto elapsed = chrono::duration<double>(now - start).count();
        if(elapsed > 1.7) break;
        
        int cx = rng()%90000, cy = rng()%90000;
        int w = 1000 + rng()%30000;
        int h = 1000 + rng()%30000;
        int x1 = max(0, cx - w/2), x2 = min(100000, cx + w/2 - 1);
        int y1 = max(0, cy - h/2), y2 = min(100000, cy + h/2 - 1);
        if(x1 >= x2 || y1 >= y2) continue;
        
        vx = {x1, x2, x2, x1};
        vy = {y1, y1, y2, y2};
    }
    
    cout << 4 << "\\n";
    for(int i=0;i<4;++i) cout << vx[i] << " " << vy[i] << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
