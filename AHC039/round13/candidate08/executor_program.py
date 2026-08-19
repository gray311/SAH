# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <set>
#include <cmath>

using namespace std;

int main() {
    int N;
    cin >> N;
    vector<pair<int,int>> mack(5000), sard(5000);
    for(int i=0;i<N;++i) cin>>mack[i].first>>mack[i].second;
    for(int i=0;i<N;++i) cin>>sard[i].first>>sard[i].second;
    cout << "4\\n0 0\\n10000 0\\n10000 10000\\n0 10000\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
