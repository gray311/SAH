# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>

using namespace std;

int main() {
    int N;
    cin >> N;
    vector<pair<int,int>> M(N), S(N);
    for(int i=0;i<N;i++) cin >> M[i].first >> M[i].second;
    for(int i=0;i<N;i++) cin >> S[i].first >> S[i].second;
    cout << "4\\n0 0\\n100000 0\\n100000 100000\\n0 100000\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
