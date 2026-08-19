# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

int main() {
    int N=5000;
    vector<pair<int,int>> fish(2*N);
    for(int i=0;i<2*N;++i) cin>>fish[i].first>>fish[i].second;
    
    cout << 4 << endl;
    cout << 0 << " " << 0 << endl;
    cout << 100000 << " " << 0 << endl;
    cout << 100000 << " " << 100000 << endl;
    cout << 0 << " " << 100000 << endl;
    return 0;
}
'''
# EVOLVE-BLOCK-END
