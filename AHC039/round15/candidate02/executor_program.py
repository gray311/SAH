# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

int N;
vector<pair<int,int>> mackerels, sardines;

int count_mackerels(int xmin, int ymin, int xmax, int ymax) {
    int cnt = 0;
    for (const auto& p : mackerels) {
        if (p.first >= xmin && p.first <= xmax && p.second >= ymin && p.second <= ymax) cnt++;
    }
    return cnt;
}

int count_sardines(int xmin, int ymin, int xmax, int ymax) {
    int cnt = 0;
    for (const auto& p : sardines) {
        if (p.first >= xmin && p.first <= xmax && p.second >= ymin && p.second <= ymax) cnt++;
    }
    return cnt;
}

int score_box(int xmin, int ymin, int xmax, int ymax) {
    return count_mackerels(xmin, ymin, xmax, ymax) - count_sardines(xmin, ymin, xmax, ymax);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    cin >> N;
    mackerels.resize(N);
    sardines.resize(N);
    
    for (int i = 0; i < N; i++) {
        cin >> mackerels[i].first >> mackerels[i].second;
    }
    for (int i = 0; i < N; i++) {
        cin >> sardines[i].first >> sardines[i].second;
    }
    
    // Try multiple box sizes and find the best one
    int best_idx = 0;
    int best_m = 0, best_s = 0, best_size = 0;
    
    // Try different box sizes
    int sizes[] = {50, 70, 90, 110, 130, 150, 170, 190, 210};
    
    for (int sz : sizes) {
        int best_local_idx = 0;
        int best_local_m = 0, best_local_s = 0;
        
        for (int i = 0; i < N; i++) {
            int m = 0, s = 0;
            int sx = mackerels[i].first - sz/2, sy = mackerels[i].second - sz/2;
            int ex = mackerels[i].first + sz/2, ey = mackerels[i].second + sz/2;
            sx = max(0, sx); sy = max(0, sy);
            ex = min(100000, ex); ey = min(100000, ey);
            
            for (const auto& p : mackerels) {
                if (p.first >= sx && p.first <= ex && p.second >= sy && p.second <= ey) m++;
            }
            for (const auto& p : sardines) {
                if (p.first >= sx && p.first <= ex && p.second >= sy && p.second <= ey) s++;
            }
            
            if (m - s > best_local_m - best_local_s) {
                best_local_m = m; best_local_s = s;
                best_local_idx = i;
            }
        }
        
        if (best_local_m - best_local_s > best_m - best_s) {
            best_m = best_local_m; best_s = best_local_s;
            best_idx = best_local_idx;
            best_size = sz;
        }
    }
    
    int sx = mackerels[best_idx].first - best_size/2;
    int sy = mackerels[best_idx].second - best_size/2;
    int ex = mackerels[best_idx].first + best_size/2;
    int ey = mackerels[best_idx].second + best_size/2;
    
    sx = max(0, sx); sy = max(0, sy);
    ex = min(100000, ex); ey = min(100000, ey);
    
    cout << 4 << "\\n";
    cout << sx << " " << sy << "\\n";
    cout << ex << " " << sy << "\\n";
    cout << ex << " " << ey << "\\n";
    cout << sx << " " << ey << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
