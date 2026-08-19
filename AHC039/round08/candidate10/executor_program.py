# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int N;
    cin >> N;
    for(int i=0;i<N;i++){int x,y;cin>>x>>y;}
    for(int i=0;i<N;i++){int x,y;cin>>x>>y;}
    
    vector<pair<int,int>> ans = {{0,0}, {50000,0}, {50000,50000}, {0,50000}};
    cout << ans.size() << endl;
    for(const auto&p : ans) cout << p.first << " " << p.second << endl;
    return 0;
}
'''
# EVOLVE-BLOCK-END
