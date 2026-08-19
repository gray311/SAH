# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <random>

using namespace std;

const int MAX_COORD = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

struct Point {
    int x, y;
    bool operator<(const Point& o) const {
        if (x != o.x) return x < o.x;
        return y < o.y;
    }
    bool operator==(const Point& o) const {
        return x == o.x && y == o.y;
    }
};

struct Fish {
    Point p;
    int type; // 1 = mackerel, -1 = sardine
};

vector<Fish> fish;

// Check if point is inside rectangle
bool point_in_rect(Point p, int x1, int y1, int x2, int y2) {
    return p.x >= x1 && p.x <= x2 && p.y >= y1 && p.y <= y2;
}

// Calculate score for rectangle: O(n)
int score_rect(int x1, int y1, int x2, int y2) {
    int m = 0, s = 0;
    for (const auto& f : fish) {
        if (point_in_rect(f.p, x1, y1, x2, y2)) {
            if (f.type == 1) m++;
            else s++;
        }
    }
    return max(0, m - s + 1);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int N;
    cin >> N;
    
    fish.resize(2 * N);
    int mx_min = MAX_COORD + 1, mx_max = -1, my_min = MAX_COORD + 1, my_max = -1;
    
    // Read mackerels
    for (int i = 0; i < N; ++i) {
        cin >> fish[i].p.x >> fish[i].p.y;
        fish[i].type = 1;
        mx_min = min(mx_min, fish[i].p.x);
        mx_max = max(mx_max, fish[i].p.x);
        my_min = min(my_min, fish[i].p.y);
        my_max = max(my_max, fish[i].p.y);
    }
    
    // Read sardines
    for (int i = 0; i < N; ++i) {
        cin >> fish[N + i].p.x >> fish[N + i].p.y;
        fish[N + i].type = -1;
    }
    
    // Try multiple starting rectangles
    int best_score = 0;
    int best_x1 = 0, best_y1 = 0, best_x2 = 0, best_y2 = 0;
    
    // Strategy 1: Bounding box of mackerels
    int x1 = mx_min, y1 = my_min, x2 = mx_max, y2 = my_max;
    int score = score_rect(x1, y1, x2, y2);
    if (score > best_score) {
        best_score = score;
        best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
    }
    
    // Strategy 2: Try expanding in different directions from mackerel bounding box
    vector<int> deltas = {1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000};
    
    for (int d : deltas) {
        // Expand right
        x1 = mx_min; y1 = my_min; x2 = min(MAX_COORD, mx_max + d); y2 = my_max;
        score = score_rect(x1, y1, x2, y2);
        if (score > best_score) {
            best_score = score;
            best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
        }
        
        // Expand left
        x1 = max(0, mx_min - d); y1 = my_min; x2 = mx_max; y2 = my_max;
        score = score_rect(x1, y1, x2, y2);
        if (score > best_score) {
            best_score = score;
            best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
        }
        
        // Expand up
        x1 = mx_min; y1 = max(0, my_min - d); x2 = mx_max; y2 = my_max;
        score = score_rect(x1, y1, x2, y2);
        if (score > best_score) {
            best_score = score;
            best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
        }
        
        // Expand down
        x1 = mx_min; y1 = my_min; x2 = mx_max; y2 = min(MAX_COORD, my_max + d);
        score = score_rect(x1, y1, x2, y2);
        if (score > best_score) {
            best_score = score;
            best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
        }
    }
    
    // Strategy 3: Try rectangles centered on mackerel clusters
    vector<int> sample_indices;
    for (int i = 0; i < N; ++i) sample_indices.push_back(i);
    shuffle(sample_indices.begin(), sample_indices.end(), default_random_engine(42));
    
    for (int i = 0; i < min((int)sample_indices.size(), 200); ++i) {
        int idx = sample_indices[i];
        int cx = fish[idx].p.x, cy = fish[idx].p.y;
        
        // Try different sizes
        for (int size = 500; size <= 100000; size *= 2) {
            x1 = max(0, cx - size/2); y1 = max(0, cy - size/2);
            x2 = min(MAX_COORD, cx + size/2); y2 = min(MAX_COORD, cy + size/2);
            score = score_rect(x1, y1, x2, y2);
            if (score > best_score) {
                best_score = score;
                best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
            }
        }
    }
    
    // Strategy 4: Try rectangles at grid points
    for (int gx = 0; gx <= MAX_COORD; gx += 5000) {
        for (int gy = 0; gy <= MAX_COORD; gy += 5000) {
            x1 = gx; y1 = gy; x2 = min(MAX_COORD, gx + 50000); y2 = min(MAX_COORD, gy + 50000);
            score = score_rect(x1, y1, x2, y2);
            if (score > best_score) {
                best_score = score;
                best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
            }
        }
    }
    
    // Strategy 5: Try rectangles with different aspect ratios
    for (int w = 1000; w <= 100000; w += 5000) {
        for (int h = 1000; h <= 100000; h += 5000) {
            // Try placing rectangle at various positions
            for (int gx = 0; gx <= MAX_COORD - w; gx += 10000) {
                for (int gy = 0; gy <= MAX_COORD - h; gy += 10000) {
                    x1 = gx; y1 = gy; x2 = gx + w; y2 = gy + h;
                    score = score_rect(x1, y1, x2, y2);
                    if (score > best_score) {
                        best_score = score;
                        best_x1 = x1; best_y1 = y1; best_x2 = x2; best_y2 = y2;
                    }
                }
            }
        }
    }
    
    // Output best rectangle
    cout << 4 << "\\n";
    cout << best_x1 << " " << best_y1 << "\\n";
    cout << best_x2 << " " << best_y1 << "\\n";
    cout << best_x2 << " " << best_y2 << "\\n";
    cout << best_x1 << " " << best_y2 << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
