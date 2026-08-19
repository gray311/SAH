# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int N;
    cin >> N;
    
    vector<pair<int,int>> M(2*N);
    for(int i=0;i<N;i++) cin>>M[i].first>>M[i].second;
    for(int i=0;i<N;i++) cin>>M[N+i].first>>M[N+i].second;
    
    // Output default polygon
    cout << "4\\n0 0\\n10000 0\\n10000 10000\\n0 10000\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
