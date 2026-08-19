# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    if (!(cin >> n)) return 0;
    
    vector<int> x(n), y(n), sx(n), sy(n);
    
    for (int i = 0; i < n; i++) {
        cin >> x[i] >> y[i];
    }
    for (int i = 0; i < n; i++) {
        cin >> sx[i] >> sy[i];
    }
    
    if (n == 0) {
        cout << "4\\n0 0\\n1 0\\n1 1\\n0 1\\n";
        return 0;
    }
    
    int minx = 200000, maxx = -1, miny = 200000, maxy = -1;
    for (int i = 0; i < n; i++) {
        minx = min(minx, x[i]); maxx = max(maxx, x[i]);
        miny = min(miny, y[i]); maxy = max(maxy, y[i]);
    }
    if (minx > maxx) minx = 0, maxx = 100000;
    if (miny > maxy) miny = 0, maxy = 100000;
    
    // Output initial bounding box of mackerels
    vector<pair<int,int>> P{{minx, miny}, {maxx, miny}, {maxx, maxy}, {minx, maxy}};
    long long perim = 2LL * (maxx - minx) + 2LL * (maxy - miny);
    
    if (perim > 400000) {
        P = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
    }
    
    cout << P.size() << "\\n";
    for (const auto& p : P) {
        cout << p.first << " " << p.second << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
