# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int N; cin >> N;
    vector<pair<int,int>> fish(2*N);
    for (int i = 0; i < N; i++) cin >> fish[i].first >> fish[i].second;
    for (int i = 0; i < N; i++) cin >> fish[N+i].first >> fish[N+i].second;
    
    // Find bounding box of mackerels
    int mx = 0, mn = 100000, my = 0, mny = 100000;
    for (int i = 0; i < N; i++) {
        mx = max(mx, fish[i].first);
        mn = min(mn, fish[i].first);
        my = max(my, fish[i].second);
        mny = min(mny, fish[i].second);
    }
    
    // Use a safe bounding box
    int sx = max(0, min(50000, mn)), ex = min(100000, max(50000, mx));
    int sy = max(0, min(50000, mny)), ey = min(100000, max(50000, my));
    
    cout << 4 << "\n";
    cout << sx << " " << sy << "\n";
    cout << ex << " " << sy << "\n";
    cout << ex << " " << ey << "\n";
    cout << sx << " " << ey << "\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
