# EVOLVE-BLOCK-START
CPP_CODE = r'''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int N;
    cin >> N;
    
    vector<pair<int,int>> M(N), S(N);
    for(int i=0;i<N;i++)cin>>M[i].first>>M[i].second;
    for(int i=0;i<N;i++)cin>>S[i].first>>S[i].second;
    
    // Output default small square
    cout << "4\n";
    cout << "0 0\n";
    cout << "100 0\n";
    cout << "100 100\n";
    cout << "0 100\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
