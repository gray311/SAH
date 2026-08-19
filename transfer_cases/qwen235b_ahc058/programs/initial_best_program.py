# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N, L, T;
    long long K;
    cin >> N >> L >> T >> K;
    vector<int> A(N);
    for (int i = 0; i < N; ++i) {
        cin >> A[i];
    }
    vector<vector<long long>> C(L, vector<long long>(N));
    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < N; ++j) {
            cin >> C[i][j];
        }
    }

    // State: B[i][j] = count of machine j^i, P[i][j] = power of machine j^i
    vector<vector<long long>> B(L, vector<long long>(N, 1));
    vector<vector<long long>> P(L, vector<long long>(N, 0));
    long long apples = K;

    // Time-based simulation for T turns
    for (int t = 0; t < T; ++t) {
        // Try to find the best machine to strengthen
        int best_i = -1, best_j = -1;
        long long best_gain = -1;

        for (int i = 0; i < L; ++i) {
            for (int j = 0; j < N; ++j) {
                long long cost = C[i][j] * (P[i][j] + 1);
                if (apples < cost) continue;

                // Estimate gain: propagate effect through levels
                long long gain = 1;
                if (i == 0) {
                    gain = A[j];
                } else {
                    // Stronger bias for higher levels to capture cascading benefits
                    gain = 1LL << (i * 5);
                }
                // Normalize by cost for efficiency, scale up to avoid truncation
                if (cost > 0) {
                    gain = (gain << 20) / cost;
                }

                if (gain > best_gain) {
                    best_gain = gain;
                    best_i = i;
                    best_j = j;
                }
            }
        }

        if (best_i == -1) {
            cout << "-1\\n";
        } else {
            cout << best_i << " " << best_j << "\\n";
            // Apply strengthening
            long long cost = C[best_i][best_j] * (P[best_i][best_j] + 1);
            apples -= cost;
            P[best_i][best_j]++;
        }

        // Apply production step
        for (int i = 0; i < L; ++i) {
            for (int j = 0; j < N; ++j) {
                if (i == 0) {
                    apples += A[j] * B[i][j] * P[i][j];
                } else {
                    B[i-1][j] += B[i][j] * P[i][j];
                }
            }
        }
    }
    return 0;
}
'''
# EVOLVE-BLOCK-END