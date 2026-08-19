# EVOLVE-BLOCK-START
"""
Debug: add verbose output and ensure format
"""
CPP_CODE = '''
#include <iostream>
#include <algorithm>
#include <vector>
#include <set>

using namespace std;

int main() {
    int N;
    cin >> N;
    
    int minx = 100001, maxx = -1, miny = 100001, maxy = -1;
    
    vector<int> mackerels_x(N), mackerels_y(N);
    for (int i = 0; i < N; i++) {
        cin >> mackerels_x[i] >> mackerels_y[i];
        minx = min(minx, mackerels_x[i]);
        maxx = max(maxx, mackerels_x[i]);
        miny = min(miny, mackerels_y[i]);
        maxy = max(maxy, mackerels_y[i]);
    }
    
    int sx[N], sy[N];
    for (int i = 0; i < N; i++) {
        cin >> sx[i] >> sy[i];
        minx = min(minx, sx[i]);
        maxx = max(maxx, sx[i]);
        miny = min(miny, sy[i]);
        maxy = max(maxy, sy[i]);
    }
    
    cout << 4 << endl;
    cout << minx << " " << miny << endl;
    cout << minx << " " << maxy << endl;
    cout << maxx << " " << maxy << endl;
    cout << maxx << " " << miny << endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
