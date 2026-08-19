# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

struct Rect { int x, y, w, h; };

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<int> x(2*n), y(2*n);
    for (int i = 0; i < n; ++i) { cin >> x[i] >> y[i]; }
    for (int i = 0; i < n; ++i) { cin >> x[n+i] >> y[n+i]; }
    
    // Find bounding box of mackerels
    int mx = 100000, my = 100000, mnx = 0, mny = 0;
    for (int i = 0; i < n; ++i) {
        mx = min(mx, x[i]);
        mnx = max(mnx, x[i]);
        my = min(my, y[i]);
        mny = max(mny, y[i]);
    }
    
    // If all mackerels at same point, use small square
    if (mx >= mnx || my >= mny) {
        cout << 4 << endl;
        cout << mx << " " << my << endl;
        cout << mx + 1 << " " << my << endl;
        cout << mx + 1 << " " << my + 1 << endl;
        cout << mx << " " << my + 1 << endl;
        return 0;
    }
    
    // Try multiple candidate rectangles and pick the best
    vector<Rect> candidates;
    candidates.push_back({mx, my, mnx - mx, mny - my});
    
    // Try expanding in all 4 directions more aggressively
    for (int d = 1; d <= 1000; ++d) {
        if (mx - d >= 0) candidates.push_back({mx - d, my, mnx - (mx - d), mny - my});
        if (mx + d <= 100000) candidates.push_back({mx, my, (mx + d) - mx, mny - my});
        if (my - d >= 0) candidates.push_back({mx, my - d, mnx - mx, (mny) - (my - d)});
        if (my + d <= 100000) candidates.push_back({mx, my, mnx - mx, (my + d) - my});
    }
    
    // Try shrinking from each side
    for (int d = 1; d <= 500; ++d) {
        if (mx + d <= mnx) candidates.push_back({mx + d, my, (mnx) - (mx + d), mny - my});
        if (my + d <= mny) candidates.push_back({mx, my + d, mnx - mx, (mny) - (my + d)});
    }
    
    // Try rectangles with different aspect ratios
    for (int rw = 1; rw <= 2000; rw += 20) {
        for (int rh = 1; rh <= 2000; rh += 20) {
            int rx = mx + (rand() % (mnx - mx + 1)) - (rw / 2);
            int ry = my + (rand() % (mny - my + 1)) - (rh / 2);
            if (rx >= 0 && rx + rw <= 100000 && ry >= 0 && ry + rh <= 100000) {
                candidates.push_back({rx, ry, rw, rh});
            }
        }
    }
    
    // Try random rectangles
    srand(1011);
    for (int r = 0; r < 5000; ++r) {
        int rx = rand() % 100001;
        int ry = rand() % 100001;
        int rw = rand() % 100001;
        int rh = rand() % 100001;
        if (rx + rw <= 100000 && ry + rh <= 100000 && rw > 0 && rh > 0) {
            candidates.push_back({rx, ry, rw, rh});
        }
    }
    
    // Evaluate each candidate
    Rect best_rect = candidates[0];
    int best_score = 0;
    
    for (auto& rect : candidates) {
        int m_count = 0, s_count = 0;
        for (int i = 0; i < n; ++i) {
            if (x[i] >= rect.x && x[i] < rect.x + rect.w && y[i] >= rect.y && y[i] < rect.y + rect.h) m_count++;
        }
        for (int i = 0; i < n; ++i) {
            if (x[n+i] >= rect.x && x[n+i] < rect.x + rect.w && y[n+i] >= rect.y && y[n+i] < rect.y + rect.h) s_count++;
        }
        int score = max(0, m_count - s_count + 1);
        if (score > best_score) {
            best_score = score;
            best_rect = rect;
        }
    }
    
    // Output best rectangle as polygon
    cout << 4 << endl;
    cout << best_rect.x << " " << best_rect.y << endl;
    cout << best_rect.x + best_rect.w << " " << best_rect.y << endl;
    cout << best_rect.x + best_rect.w << " " << best_rect.y + best_rect.h << endl;
    cout << best_rect.x << " " << best_rect.y + best_rect.h << endl;
    return 0;
}
'''
# EVOLVE-BLOCK-END
