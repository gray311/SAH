# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAXC = 100000;
const int GRID = 205;

int grid[GRID][GRID];

int main() {
    ios::sync_with_stdio(0); cin.tie(0);
    int N; cin >> N;
    vector<int> fx(2*N), fy(2*N), ft(2*N);
    for (int i=0; i<N; i++) { cin >> fx[i] >> fy[i]; ft[i] = 1; }
    for (int i=0; i<N; i++) { cin >> fx[N+i] >> fy[N+i]; ft[N+i] = -1; }
    
    // Map to grid
    for (int i=0; i<GRID; i++) grid[i][i] = 0;
    for (int i=0; i<(int)fx.size(); i++) {
        int gx = min((int)GRID-1, fx[i]/1000);
        int gy = min((int)GRID-1, fy[i]/1000);
        grid[gx][gy] += ft[i];
    }
    
    // 2D prefix sum
    for (int i=0; i<GRID; i++) {
        for (int j=0; j<GRID; j++) {
            grid[i][j] += (i>0?grid[i-1][j]:0) + (j>0?grid[i][j-1]:0) - (i>0&&j>0?grid[i-1][j-1]:0);
        }
    }
    
    auto query = [&](int gx1, int gy1, int gx2, int gy2) {
        if (gx1 > gx2 || gy1 > gy2) return 0;
        gx1 = max(0, gx1); gy1 = max(0, gy1);
        gx2 = min(GRID-1, gx2); gy2 = min(GRID-1, gy2);
        return grid[gx2][gy2] - (gx1>0?grid[gx1-1][gy2]:0) - (gy1>0?grid[gx2][gy1-1]:0) + (gx1>0&&gy1>0?grid[gx1-1][gy1-1]:0);
    };
    
    int best = 0;
    int blx=0, bry=0, brx=1, byr=1;
    
    // Search all grid combinations with 1000 resolution
    int limx = min(100, GRID), limy = min(100, GRID);
    
    for (int i=0; i<limx; i++) {
        for (int j=i+1; j<limx; j++) {
            for (int k=0; k<limy; k++) {
                for (int l=k+1; l<limy; l++) {
                    int lx = i*1000, rx = j*1000, ly = k*1000, ry = l*1000;
                    if (lx >= rx || ly >= ry) continue;
                    int sc = query(i, k, j, l);
                    if (sc > best) { best = sc; blx=lx; bry=ly; brx=rx; byr=ry; }
                }
            }
        }
    }
    
    cout << 4 << "\\n";
    cout << blx << " " << bry << "\\n";
    cout << brx << " " << bry << "\\n";
    cout << brx << " " << byr << "\\n";
    cout << blx << " " << byr << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
