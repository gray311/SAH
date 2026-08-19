# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <cmath>

const int MAX_COORD = 100000;
const int MAX_PERIMETER = 400000;

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    std::cin >> N;
    
    std::vector<std::pair<int,int>> mackerels(N), sardines(N);
    
    for (int i = 0; i < N; ++i) {
        std::cin >> mackerels[i].first >> mackerels[i].second;
    }
    for (int i = 0; i < N; ++i) {
        std::cin >> sardines[i].first >> sardines[i].second;
    }
    
    // Find min/max coordinates
    int min_x = MAX_COORD, max_x = -1, min_y = MAX_COORD, max_y = -1;
    for (auto& p : mackerels) {
        min_x = std::min(min_x, p.first);
        max_x = std::max(max_x, p.first);
        min_y = std::min(min_y, p.second);
        max_y = std::max(max_y, p.second);
    }
    
    // If no mackerels, output default rectangle
    if (max_x < 0) {
        std::cout << 4 << "\\n";
        std::cout << "0 0\\n";
        std::cout << "1 0\\n";
        std::cout << "1 1\\n";
        std::cout << "0 1\\n";
        return 0;
    }
    
    // Build coordinate sets from mackerels
    std::vector<int> x_coords, y_coords;
    std::set<int> x_set, y_set;
    for (auto& p : mackerels) {
        x_set.insert(p.first);
        y_set.insert(p.second);
    }
    
    int limit = std::min(50, (int)x_set.size());
    std::vector<int> unique_x(x_set.begin(), x_set.end());
    std::vector<int> unique_y(y_set.begin(), y_set.end());
    std::sort(unique_x.rbegin(), unique_x.rend());
    std::sort(unique_y.rbegin(), unique_y.rend());
    
    for (int i = 0; i < limit; ++i) {
        unique_x.push_back(unique_x[unique_x.size() - 1 - i]);
        unique_y.push_back(unique_y[unique_y.size() - 1 - i]);
    }
    unique_x.resize(limit);
    unique_y.resize(limit);
    
    // Simple greedy: try rectangles from top coordinate pairs
    int best_x1 = min_x, best_y1 = min_y, best_x2 = max_x, best_y2 = max_y;
    int best_score = 0;
    
    // Try a few candidate rectangles
    for (int i = 0; i < (int)unique_x.size() && i < 20; ++i) {
        for (int j = i + 1; j < (int)unique_x.size() && j < 20; ++j) {
            int x1 = unique_x[i], x2 = unique_x[j];
            for (int k = 0; k < (int)unique_y.size() && k < 20; ++k) {
                for (int l = k + 1; l < (int)unique_y.size() && l < 20; ++l) {
                    int y1 = unique_y[k], y2 = unique_y[l];
                    
                    int perim = 2 * ((x2 - x1) + (y2 - y1));
                    if (perim > MAX_PERIMETER) continue;
                    
                    // Count using O(N) scan (acceptable for limited iterations)
                    int m_count = 0, s_count = 0;
                    for (auto& p : mackerels) {
                        if (p.first >= x1 && p.first <= x2 && p.second >= y1 && p.second <= y2) {
                            m_count++;
                        }
                    }
                    for (auto& p : sardines) {
                        if (p.first >= x1 && p.first <= x2 && p.second >= y1 && p.second <= y2) {
                            s_count++;
                        }
                    }
                    
                    int score = m_count - s_count + 1;
                    if (score > best_score) {
                        best_score = score;
                        best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
                    }
                }
            }
        }
    }
    
    std::cout << 4 << "\\n";
    std::cout << best_x1 << " " << best_y1 << "\\n";
    std::cout << best_x2 << " " << best_y1 << "\\n";
    std::cout << best_x2 << " " << best_y2 << "\\n";
    std::cout << best_x1 << " " << best_y2 << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
