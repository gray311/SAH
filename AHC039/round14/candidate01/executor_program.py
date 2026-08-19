# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>

using namespace std;

const int MAXC = 100000;
const int MAXV = 1000;
const int MAXP = 400000;

struct Fish { int x, y, t; };
vector<Fish> fish;
int N;

struct Point { int x, y; };

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    cin >> N;
    fish.resize(2 * N);
    for (int i = 0; i < N; i++) {
        cin >> fish[i].x >> fish[i].y;
        fish[i].t = 1;
    }
    for (int i = 0; i < N; i++) {
        cin >> fish[N + i].x >> fish[N + i].y;
        fish[N + i].t = -1;
    }
    
    int minx = MAXC, maxx = 0, miny = MAXC, maxy = 0;
    for (int i = 0; i < N; i++) {
        minx = min(minx, fish[i].x);
        maxx = max(maxx, fish[i].x);
        miny = min(miny, fish[i].y);
        maxy = max(maxy, fish[i].y);
    }
    
    minx = max(0, minx - 500);
    maxx = min(MAXC, maxx + 500);
    miny = max(0, miny - 500);
    maxy = min(MAXC, maxy + 500);
    
    if (minx >= maxx || miny >= maxy) {
        minx = 0; maxx = 1000;
        miny = 0; maxy = 1000;
    }
    
    cout << 4 << "\n";
    cout << minx << " " << miny << "\n";
    cout << maxx << " " << miny << "\n";
    cout << maxx << " " << maxy << "\n";
    cout << minx << " " << maxy << "\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
