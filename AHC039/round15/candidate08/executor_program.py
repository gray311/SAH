# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <bits/stdc++.h>
using namespace std;

int main() {
    int N;
    cin >> N;
    vector<pair<int,int>> macks(N), sardines(N);
    
    for (int i = 0; i < N; ++i) cin >> macks[i].first >> macks[i].second;
    for (int i = 0; i < N; ++i) cin >> sardines[i].first >> sardines[i].second;
    
    vector<pair<int,int>> poly = {{0,0}, {1,0}, {1,1}, {0,1}};
    
    cout << poly.size() << "\n";
    for (const auto& p : poly) cout << p.first << " " << p.second << "\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
