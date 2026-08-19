# EVOLVE-BLOCK-START
CPP_CODE = R'''
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int N;
    cin >> N;
    
    vector<int> mx(100001, 0), my(100001, 0);
    vector<int> M, S;
    
    for(int i = 0; i < N; i++) {
        int x, y;
        cin >> x >> y;
        M.push_back(x * 100000 + y);
        mx[x]++;
        my[y]++;
    }
    
    for(int i = 0; i < N; i++) {
        int x, y;
        cin >> x >> y;
        S.push_back(x * 100000 + y);
        mx[x]--;
        my[y]--;
    }
    
    int best_score = 0;
    int best_x1 = 0, best_y1 = 0, best_x2 = 100000, best_y2 = 100000;
    
    for(int x1 = 0; x1 <= 100000; x1 += 1000) {
        for(int y1 = 0; y1 <= 100000; y1 += 1000) {
            int x2 = min(x1 + 99999, 100000);
            int y2 = min(y1 + 99999, 100000);
            
            int score = 0;
            for(int m : M) {
                if(m >= x1 * 100000 + y1 && m <= x2 * 100000 + y2) score++;
            }
            for(int s : S) {
                if(s >= x1 * 100000 + y1 && s <= x2 * 100000 + y2) score--;
            }
            
            if(score > best_score) {
                best_score = score;
                best_x1 = x1;
                best_y1 = y1;
                best_x2 = x2;
                best_y2 = y2;
            }
        }
    }
    
    vector<pair<int, int>> v;
    v.push_back({best_x1, best_y1});
    v.push_back({best_x2, best_y1});
    v.push_back({best_x2, best_y2});
    v.push_back({best_x1, best_y2});
    
    cout << v.size() << "\n";
    for(auto p : v) cout << p.first << " " << p.second << "\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
