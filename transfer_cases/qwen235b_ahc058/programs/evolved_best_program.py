# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

double rand_double(double L, double U) {
    return L + (U - L) * rand() / RAND_MAX;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N = 10, L = 4, T = 500;
    ll K;
    cin >> N >> L >> T >> K;
    
    vector<int> A(N);
    for (int i = 0; i < N; ++i) {
        cin >> A[i];
    }
    
    vector<vector<ll>> C(L, vector<ll>(N));
    for (int i = 0; i < L; ++i) {
        for (int j = 0; j < N; ++j) {
            cin >> C[i][j];
        }
    }
    
    vector<vector<ll>> B(L, vector<ll>(N, 1));
    vector<vector<ll>> P(L, vector<ll>(N, 0));
    ll apples = K;
    
    // Multi-policy simulation with different strategies
    auto simulate_with_policy = [&](int start_turn, vector<vector<ll>> B_local, vector<vector<ll>> P_local, ll apples_local, int policy) -> ll {
        for (int t = start_turn; t < T; ++t) {
            vector<pair<int, int>> candidates;
            
            // Policy 0: Early L0 Builder (safe apple base)
            if (policy == 0) {
                if (apples_local < 1000) {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[0][j] * (P_local[0][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(0, j);
                        }
                    }
                } else {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[3][j] * (P_local[3][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(3, j);
                        }
                    }
                }
            }
            // Policy 1: Aggressive L3 (invest as soon as possible)
            else if (policy == 1) {
                for (int j = 0; j < N; ++j) {
                    ll cost = C[3][j] * (P_local[3][j] + 1);
                    if (apples_local >= cost) {
                        candidates.emplace_back(3, j);
                    }
                }
                // Fallback to L0 if no L3 affordable
                if (candidates.empty()) {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[0][j] * (P_local[0][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(0, j);
                        }
                    }
                }
            }
            // Policy 2: Conservative L3 (high threshold)
            else if (policy == 2) {
                if (apples_local >= 100000) {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[3][j] * (P_local[3][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(3, j);
                        }
                    }
                } else {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[0][j] * (P_local[0][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(0, j);
                        }
                    }
                }
            }
            // Policy 3: Balanced Cascade (alternate focus)
            else if (policy == 3) {
                double r = rand_double(0, 1);
                if (r < 0.5 && apples_local >= 1000) {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[3][j] * (P_local[3][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(3, j);
                        }
                    }
                } else {
                    for (int j = 0; j < N; ++j) {
                        ll cost = C[0][j] * (P_local[0][j] + 1);
                        if (apples_local >= cost) {
                            candidates.emplace_back(0, j);
                        }
                    }
                }
            }
            
            // Apply best candidate if available
            if (!candidates.empty()) {
                // Sort by cost-effectiveness
                sort(candidates.begin(), candidates.end(), [&](auto &a, auto &b) {
                    int i1 = a.first, j1 = a.second;
                    int i2 = b.first, j2 = b.second;
                    double score1 = (i1 == 0) ? (double)A[j1] / (C[i1][j1] * (P_local[i1][j1] + 1)) : 1e6 / (C[i1][j1] * (P_local[i1][j1] + 1));
                    double score2 = (i2 == 0) ? (double)A[j2] / (C[i2][j2] * (P_local[i2][j2] + 1)) : 1e6 / (C[i2][j2] * (P_local[i2][j2] + 1));
                    return score1 > score2;
                });
                
                int i = candidates[0].first;
                int j = candidates[0].second;
                ll cost = C[i][j] * (P_local[i][j] + 1);
                if (apples_local >= cost) {
                    apples_local -= cost;
                    P_local[i][j]++;
                }
            }
            
            // Cascade phase
            for (int i = 0; i < L; ++i) {
                if (i == 0) {
                    for (int j = 0; j < N; ++j) {
                        apples_local += (ll)A[j] * B_local[i][j] * P_local[i][j];
                    }
                } else {
                    for (int j = 0; j < N; ++j) {
                        B_local[i-1][j] += B_local[i][j] * P_local[i][j];
                    }
                }
            }
        }
        return apples_local;
    };
    
    vector<string> actions(T);
    
    for (int t = 0; t < T; ++t) {
        // Use action_analyzer to get pruned list - replaced with internal heuristic
        vector<pair<int, int>> candidates;
        vector<double> scores;
        
        // Generate candidates with heuristic scoring
        for (int i = 0; i < L; ++i) {
            for (int j = 0; j < N; ++j) {
                ll cost = C[i][j] * (P[i][j] + 1);
                if (apples >= cost) {
                    double score = 0;
                    if (i == 0) score = (double)A[j] * 1000 / cost;  // High weight for L0
                    else if (i == 3) score = 1e6 / cost;  // Very high potential for L3
                    else score = 1.0 / cost;  // Lower levels less important
                    
                    // Insert in sorted order (top 22)
                    auto it = lower_bound(scores.begin(), scores.end(), score, greater<double>());
                    int idx = it - scores.begin();
                    if (scores.size() < 22) {
                        scores.insert(it, score);
                        candidates.emplace(candidates.begin() + idx, i, j);
                    } else if (idx < 22) {
                        scores.insert(it, score);
                        candidates.emplace(candidates.begin() + idx, i, j);
                        scores.pop_back();
                        candidates.pop_back();
                    }
                }
            }
        }
        
        ll best_final = apples;
        pair<int, int> best_action = {-1, -1};
        
        // Test doing nothing
        {
            auto B_copy = B;
            auto P_copy = P;
            ll sim_apples = apples;
            
            // Try each policy for do-nothing
            for (int policy = 0; policy < 4; ++policy) {
                ll final_apples = simulate_with_policy(t+1, B_copy, P_copy, sim_apples, policy);
                if (final_apples > best_final) {
                    best_final = final_apples;
                    best_action = {-1, -1};
                }
            }
        }
        
        // Test each candidate action with multi-policy simulation
        for (int c = 0; c < candidates.size(); ++c) {
            int i = candidates[c].first;
            int j = candidates[c].second;
            ll cost = C[i][j] * (P[i][j] + 1);
            if (apples < cost) continue;
            
            auto B_copy = B;
            auto P_copy = P;
            ll sim_apples = apples;
            
            // Apply action
            sim_apples -= cost;
            P_copy[i][j]++;
            
            // Cascade after action
            for (int lvl = 0; lvl < L; ++lvl) {
                if (lvl == 0) {
                    for (int jj = 0; jj < N; ++jj) {
                        sim_apples += (ll)A[jj] * B_copy[lvl][jj] * P_copy[lvl][jj];
                    }
                } else {
                    for (int jj = 0; jj < N; ++jj) {
                        B_copy[lvl-1][jj] += B_copy[lvl][jj] * P_copy[lvl][jj];
                    }
                }
            }
            
            // Try each policy variant and take best
            ll best_policy_result = sim_apples;
            for (int policy = 0; policy < 4; ++policy) {
                ll final_apples = simulate_with_policy(t+1, B_copy, P_copy, sim_apples, policy);
                if (final_apples > best_policy_result) {
                    best_policy_result = final_apples;
                }
            }
            
            if (best_policy_result > best_final) {
                best_final = best_policy_result;
                best_action = {i, j};
            }
        }
        
        // Execute best action
        if (best_action.first == -1) {
            actions[t] = "-1";
        } else {
            int i = best_action.first;
            int j = best_action.second;
            ll cost = C[i][j] * (P[i][j] + 1);
            apples -= cost;
            P[i][j]++;
            actions[t] = to_string(i) + " " + to_string(j);
        }
        
        // Final cascade for the turn
        for (int i = 0; i < L; ++i) {
            if (i == 0) {
                for (int j = 0; j < N; ++j) {
                    apples += (ll)A[j] * B[i][j] * P[i][j];
                }
            } else {
                for (int j = 0; j < N; ++j) {
                    B[i-1][j] += B[i][j] * P[i][j];
                }
            }
        }
    }
    
    for (int t = 0; t < T; ++t) {
        cout << actions[t] << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END