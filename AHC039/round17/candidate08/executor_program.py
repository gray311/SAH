# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int N;
    cin >> N;
    
    vector<pair<int, int>> mackerels(N);
    vector<pair<int, int>> sardines(N);
    
    for (int i = 0; i < N; i++) cin >> mackerels[i].first >> mackerels[i].second;
    for (int i = 0; i < N; i++) cin >> sardines[i].first >> sardines[i].second;
    
    // Output a simple 1x1 square at origin
    cout << 4 << endl;
    cout << 0 << " " << 0 << endl;
    cout << 1 << " " << 0 << endl;
    cout << 1 << " " << 1 << endl;
    cout << 0 << " " << 1 << endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
