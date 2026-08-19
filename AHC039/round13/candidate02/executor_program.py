# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    vector<pair<int,int>> mackerels(N), sardines(N);
    for(int i=0; i<N; i++) {
        int x, y;
        cin >> x >> y;
        mackerels[i] = {x, y};
    }
    for(int i=0; i<N; i++) {
        int x, y;
        cin >> x >> y;
        sardines[i] = {x, y};
    }
    
    int best_score = -1000000;
    int best_x1 = 0, best_y1 = 0, best_x2 = 0, best_y2 = 0;
    
    // Try many random rectangles
    for(int iter = 0; iter < 5000; iter++) {
        int x1 = rand() % 100001;
        int y1 = rand() % 100001;
        int x2 = min(100000, x1 + 1 + rand() % 99998);
        int y2 = min(100000, y1 + 1 + rand() % 99998);
        
        int m = 0, s = 0;
        for(auto& p : mackerels) {
            if(p.first >= x1 && p.first <= x2 && p.second >= y1 && p.second <= y2) m++;
        }
        for(auto& p : sardines) {
            if(p.first >= x1 && p.first <= x2 && p.second >= y1 && p.second <= y2) s++;
        }
        
        int score = m - s;
        if(score > best_score) {
            best_score = score;
            best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
        }
    }
    
    cout << 4 << "\\n";
    cout << best_x1 << " " << best_y1 << "\\n";
    cout << best_x2 << " " << best_y1 << "\\n";
    cout << best_x2 << " " << best_y2 << "\\n";
    cout << best_x1 << " " << best_y2 << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
