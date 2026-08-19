# EVOLVE-BLOCK-START
CPP_CODE = '''#include <bits/stdc++.h>
using namespace std;

int main() {
    int N;
    if (!(cin >> N)) return 0;
    vector<pair<int,int>> f(2*N);
    for(int i=0;i<2*N;++i) cin >> f[i].first >> f[i].second;
    
    vector<pair<int,int>> poly;
    poly.push_back({0, 0});
    poly.push_back({100000, 0});
    poly.push_back({100000, 100000});
    poly.push_back({0, 100000});
    
    cout << poly.size() << endl;
    for(auto& p : poly) cout << p.first << " " << p.second << endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
