# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>

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
    int type; // 1=mackerel, -1=sardine
};

vector<Fish> fish;
vector<Point> polygon;

// Check if point is inside polygon (ray casting)
bool point_in_polygon(Point p, const vector<Point>& poly) {
    int n = poly.size();
    if (n < 3) return false;
    bool inside = false;
    for (int i = 0, j = n - 1; i < n; j = i++) {
        if (((poly[i].y > p.y) != (poly[j].y > p.y)) &&
            (p.x < (poly[j].x - poly[i].x) * (double)(p.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)) {
            inside = !inside;
        }
    }
    return inside;
}

// Check if point is on boundary
bool point_on_boundary(Point p, const vector<Point>& poly) {
    int n = poly.size();
    for (int i = 0; i < n; i++) {
        Point a = poly[i];
        Point b = poly[(i + 1) % n];
        if (a.x == b.x) {
            if (p.x == a.x && p.y >= min(a.y, b.y) && p.y <= max(a.y, b.y)) return true;
        } else {
            if (p.y == a.y && p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x)) return true;
        }
    }
    return false;
}

// Calculate score
int calculate_score() {
    int m_count = 0, s_count = 0;
    for (const auto& f : fish) {
        if (point_in_polygon(f.p, polygon) || point_on_boundary(f.p, polygon)) {
            if (f.type == 1) m_count++;
            else s_count++;
        }
    }
    return max(0, m_count - s_count + 1);
}

// Find best rectangle using a very coarse grid
void find_best_rectangle() {
    if (fish.empty()) {
        polygon = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
        return;
    }
    
    // Use a coarse grid for speed - 12x12 grid
    const int GRID_SIZE = 12;
    const int CELL_SIZE = MAX_COORD / GRID_SIZE;
    
    // Count mackerels and sardines in each cell
    vector<vector<int>> cell_score(GRID_SIZE, vector<int>(GRID_SIZE, 0));
    vector<vector<int>> cell_mackerel(GRID_SIZE, vector<int>(GRID_SIZE, 0));
    vector<vector<int>> cell_sardine(GRID_SIZE, vector<int>(GRID_SIZE, 0));
    
    for (const auto& f : fish) {
        int gx = f.p.x / CELL_SIZE;
        int gy = f.p.y / CELL_SIZE;
        gx = min(gx, GRID_SIZE - 1);
        gy = min(gy, GRID_SIZE - 1);
        if (f.type == 1) {
            cell_mackerel[gx][gy]++;
            cell_score[gx][gy]++;
        } else {
            cell_sardine[gx][gy]++;
            cell_score[gx][gy]--;
        }
    }
    
    // Find best rectangle of cells (try 1x1 to 15x15)
    int best_gx = -1, best_gy = -1;
    int best_w = 1, best_h = 1;
    int best_score = -1e9;
    
    // Try all possible rectangle sizes
    for (int w = 1; w <= 15; w++) {
        for (int h = 1; h <= 15; h++) {
            for (int gx = 0; gx <= GRID_SIZE - w; gx++) {
                for (int gy = 0; gy <= GRID_SIZE - h; gy++) {
                    int score = 0;
                    bool has_mackerel = false;
                    for (int dw = 0; dw < w; dw++) {
                        for (int dh = 0; dh < h; dh++) {
                            score += cell_score[gx + dw][gy + dh];
                            if (cell_mackerel[gx + dw][gy + dh] > 0) has_mackerel = true;
                        }
                    }
                    if (has_mackerel && score > best_score) {
                        best_score = score;
                        best_gx = gx;
                        best_gy = gy;
                        best_w = w;
                        best_h = h;
                    }
                }
            }
        }
    }
    
    if (best_gx == -1) {
        polygon = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
        return;
    }
    
    // Create polygon around best rectangle
    int min_x = best_gx * CELL_SIZE;
    int max_x = min(MAX_COORD, (best_gx + best_w) * CELL_SIZE);
    int min_y = best_gy * CELL_SIZE;
    int max_y = min(MAX_COORD, (best_gy + best_h) * CELL_SIZE);
    
    polygon = {{min_x, min_y}, {max_x, min_y}, {max_x, max_y}, {min_x, max_y}};
}

// Expand polygon to include more mackerels
void expand_polygon() {
    if (fish.empty()) return;
    
    int min_x = polygon[0].x, max_x = polygon[1].x;
    int min_y = polygon[0].y, max_y = polygon[2].y;
    
    int best_score = calculate_score();
    
    // Try expanding in each direction - more iterations for speed
    for (int iter = 0; iter < 150; iter++) {
        int current_score = calculate_score();
        if (current_score <= best_score) break;
        best_score = current_score;
        
        // Try expanding right
        int new_max_x = max_x + 1;
        if (new_max_x <= MAX_COORD && 
            (long long)(new_max_x - min_x) * (max_y - min_y) * 2 <= MAX_PERIMETER) {
            polygon[1].x = new_max_x;
            polygon[2].x = new_max_x;
        }
        
        // Try expanding left
        int new_min_x = min_x - 1;
        if (new_min_x >= 0 &&
            (long long)(max_x - new_min_x) * (max_y - min_y) * 2 <= MAX_PERIMETER) {
            polygon[0].x = new_min_x;
            polygon[3].x = new_min_x;
        }
        
        // Try expanding up
        int new_max_y = max_y + 1;
        if (new_max_y <= MAX_COORD &&
            (long long)(max_x - min_x) * (new_max_y - min_y) * 2 <= MAX_PERIMETER) {
            polygon[2].y = new_max_y;
            polygon[3].y = new_max_y;
        }
        
        // Try expanding down
        int new_min_y = min_y - 1;
        if (new_min_y >= 0 &&
            (long long)(max_x - min_x) * (max_y - new_min_y) * 2 <= MAX_PERIMETER) {
            polygon[0].y = new_min_y;
            polygon[1].y = new_min_y;
        }
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int N;
    cin >> N;
    
    fish.resize(2 * N);
    for (int i = 0; i < N; i++) {
        cin >> fish[i].p.x >> fish[i].p.y;
        fish[i].type = 1;
    }
    for (int i = 0; i < N; i++) {
        cin >> fish[N + i].p.x >> fish[N + i].p.y;
        fish[N + i].type = -1;
    }
    
    find_best_rectangle();
    expand_polygon();
    
    cout << polygon.size() << "\\n";
    for (const auto& p : polygon) {
        cout << p.x << " " << p.y << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
