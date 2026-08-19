# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <chrono>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    if (!(cin >> N)) return 0;
    
    vector<int> X(2 * N), Y(2 * N);
    int typ[20000];
    
    for (int i = 0; i < N; i++) {
        cin >> X[i] >> Y[i];
        typ[i] = 1;
    }
    for (int i = 0; i < N; i++) {
        cin >> X[N + i] >> Y[N + i];
        typ[N + i] = -1;
    }
    
    int best = INT_MIN;
    int P[4][2];
    P[0][0] = 0; P[0][1] = 0;
    P[1][0] = 1; P[1][1] = 0;
    P[2][0] = 1; P[2][1] = 1;
    P[3][0] = 0; P[3][1] = 1;
    
    int seeds_x[30] = {0, 2000, 4000, 6000, 8000, 
                       0, 2000, 4000, 6000, 8000,
                       0, 2000, 4000, 6000, 8000,
                       0, 2000, 4000, 6000, 8000,
                       0, 2000, 4000, 6000, 8000,
                       10000, 0, 2000, 4000};
    int seeds_y[30] = {0, 0, 0, 0, 0,
                        2000, 2000, 2000, 2000, 2000,
                        4000, 4000, 4000, 4000, 4000,
                        6000, 6000, 6000, 6000, 6000,
                        8000, 8000, 8000, 8000, 8000,
                        10000, 0, 2000, 0, 2000};
    
    auto t = chrono::steady_clock::now();
    
    for (int rst = 0; rst < 15 && chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - t).count() < 1500; rst++) {
        int gx_min = std::max(0, seeds_x[rst % 15] - 5000);
        int gy_min = std::max(0, seeds_y[rst % 15] - 5000);
        int gx_max = seeds_x[rst % 15] + 8000;
        int gy_max = seeds_y[rst % 15] + 8000;
        if (gx_min > gx_max) gx_max = gx_min;
        if (gy_min > gy_max) gy_max = gy_min;
        gx_max = std::min(gx_max, 100000);
        gy_max = std::min(gy_max, 100000);
        
        for (int gx = gx_min; gx <= gx_max; gx += 1500) {
            for (int gy = gy_min; gy <= gy_max; gy += 1500) {
                for (int ex = gx; ex <= std::min(gx + 12000, 100000); ex += 2000) {
                    for (int ey = gy; ey <= std::min(gy + 12000, 100000); ey += 2000) {
                        if (ex < gx || ey < gy) continue;
                        
                        int mm = 0, ss = 0;
                        for (int j = 0; j < 2 * N; j++) {
                            if (X[j] >= gx && X[j] <= ex && Y[j] >= gy && Y[j] <= ey) {
                                mm += typ[j]; ss = 0; // simplified
                            }
                        }
                        int sc = (mm > 0) ? mm + 1 : 0;
                        if (sc > best) {
                            best = sc;
                            P[0][0] = gx; P[0][1] = gy;
                            P[1][0] = ex; P[1][1] = gy;
                            P[2][0] = ex; P[2][1] = ey;
                            P[3][0] = gx; P[3][1] = ey;
                        }
                    }
                }
            }
        }
    }
    
    cout << "4\n";
    for (int i = 0; i < 4; i++) cout << P[i][0] << " " << P[i][1] << "\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
