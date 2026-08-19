# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;
const int GRID_SIZE = 100;
const int CELL_SIZE = 1000;

struct Fish {
    int x, y, type;
};
vector<Fish> fish_data;
int N;

int grid_m[GRID_SIZE][GRID_SIZE];
int grid_s[GRID_SIZE][GRID_SIZE];
int grid_score[GRID_SIZE][GRID_SIZE];

struct Point {
    int x, y;
    bool operator<(const Point& o) const { return x < o.x || (x == o.x && y < o.y); }
};

long long calc_perimeter(const vector<Point>& poly) {
    if (poly.size() < 2) return 0;
    long long p = 0;
    for (size_t i = 0; i < poly.size(); i++) {
        Point p1 = poly[i];
        Point p2 = poly[(i + 1) % poly.size()];
        p += abs(p1.x - p2.x) + abs(p1.y - p2.y);
    }
    return p;
}

bool is_valid(const vector<Point>& poly) {
    if (poly.size() < 4 || poly.size() > MAX_VERTICES) return false;
    if (calc_perimeter(poly) > MAX_PERIMETER) return false;
    set<Point> pts;
    for (const auto& p : poly) {
        if (p.x < 0 || p.x > MAX_COORD_VAL || p.y < 0 || p.y > MAX_COORD_VAL) return false;
        if (!pts.insert(p).second) return false;
    }
    return true;
}

void build_grid() {
    for (int i = 0; i < GRID_SIZE; i++)
        for (int j = 0; j < GRID_SIZE; j++) {
            grid_m[i][j] = 0;
            grid_s[i][j] = 0;
        }
    for (const auto& f : fish_data) {
        int r = f.y / CELL_SIZE;
        int c = f.x / CELL_SIZE;
        r = min(GRID_SIZE - 1, max(0, r));
        c = min(GRID_SIZE - 1, max(0, c));
        if (f.type == 1) grid_m[r][c]++;
        else grid_s[r][c]++;
    }
    for (int i = 0; i < GRID_SIZE; i++)
        for (int j = 0; j < GRID_SIZE; j++)
            grid_score[i][j] = grid_m[i][j] - grid_s[i][j];
}

vector<pair<int, int>> expand_corridor(int start_r, int start_c, int dir, int max_len) {
    vector<pair<int, int>> path;
    int r = start_r, c = start_c;
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    for (int k = 0; k < max_len; k++) {
        if (r < 0 || r >= GRID_SIZE || c < 0 || c >= GRID_SIZE) break;
        if (grid_score[r][c] < 0) break;
        if (grid_s[r][c] > grid_m[r][c] + 2) break;
        path.push_back({r, c});
        r += dr[dir];
        c += dc[dir];
    }
    return path;
}

vector<Point> build_poly_from_seeds(int seed_r, int seed_c) {
    vector<vector<pair<int, int>>> corridors(4);
    for (int d = 0; d < 4; d++) {
        corridors[d] = expand_corridor(seed_r, seed_c, d, 50);
    }
    
    vector<Point> poly;
    bool has_corridor = false;
    for (int d = 0; d < 4; d++) {
        if (!corridors[d].empty()) has_corridor = true;
    }
    
    if (has_corridor) {
        int min_r = GRID_SIZE, max_r = -1, min_c = GRID_SIZE, max_c = -1;
        for (int d = 0; d < 4; d++) {
            for (const auto& p : corridors[d]) {
                min_r = min(min_r, p.first);
                max_r = max(max_r, p.first);
                min_c = min(min_c, p.second);
                max_c = max(max_c, p.second);
            }
        }
        if (min_r <= max_r && min_c <= max_c) {
            poly.push_back({min_c * CELL_SIZE, min_r * CELL_SIZE});
            poly.push_back({max_c * CELL_SIZE, min_r * CELL_SIZE});
            poly.push_back({max_c * CELL_SIZE, max_r * CELL_SIZE});
            poly.push_back({min_c * CELL_SIZE, max_r * CELL_SIZE});
        }
    }
    
    if (poly.empty()) {
        poly.push_back({seed_c * CELL_SIZE, seed_r * CELL_SIZE});
        poly.push_back({(seed_c + 1) * CELL_SIZE, seed_r * CELL_SIZE});
        poly.push_back({(seed_c + 1) * CELL_SIZE, (seed_r + 1) * CELL_SIZE});
        poly.push_back({seed_c * CELL_SIZE, (seed_r + 1) * CELL_SIZE});
    }
    
    return poly;
}

long long calc_score(const vector<Point>& poly) {
    if (poly.size() < 4) return -1e9;
    long long m = 0, s = 0;
    for (size_t i = 0; i < poly.size(); i++) {
        Point p1 = poly[i];
        Point p2 = poly[(i + 1) % poly.size()];
        int r1 = min(p1.y, p2.y) / CELL_SIZE;
        int r2 = max(p1.y, p2.y) / CELL_SIZE;
        int c1 = min(p1.x, p2.x) / CELL_SIZE;
        int c2 = max(p1.x, p2.x) / CELL_SIZE;
        for (int r = r1; r <= r2; r++)
            for (int c = c1; c <= c2; c++) {
                m += grid_m[r][c];
                s += grid_s[r][c];
            }
    }
    return m - s;
}

vector<Point> hill_climb(vector<Point> poly, int& best_m, int& best_s) {
    int best_val = -1e9;
    vector<Point> best_poly = poly;
    
    // Multiple rounds of hill climbing with increasing shifts
    for (int iter = 0; iter < 5; iter++) {
        vector<Point> curr = best_poly;
        long long best_curr_score = calc_score(curr);
        
        int shifts[5][2] = {{-5, 5}, {-10, 10}, {-15, 15}, {-20, 20}, {-25, 25}};
        for (int shift_idx = 0; shift_idx < 5; shift_idx++) {
            int s1 = shifts[shift_idx][0];
            int s2 = shifts[shift_idx][1];
            
            for (size_t i = 0; i < curr.size(); i++) {
                Point p1 = curr[i];
                Point p2 = curr[(i + 1) % curr.size()];
                int dx = p2.x - p1.x;
                int dy = p2.y - p1.y;
                
                // Try both directions
                for (int shift : {s1, s2}) {
                    vector<Point> test = curr;
                    if (dx == 0) {
                        int nx = p1.x + shift;
                        if (nx < 0 || nx > MAX_COORD_VAL) continue;
                        test[i].x = nx;
                        test[(i + 1) % curr.size()].x = nx;
                    } else {
                        int ny = p1.y + shift;
                        if (ny < 0 || ny > MAX_COORD_VAL) continue;
                        test[i].y = ny;
                        test[(i + 1) % curr.size()].y = ny;
                    }
                    if (!is_valid(test)) continue;
                    long long s = calc_score(test);
                    if (s > best_curr_score) {
                        best_curr_score = s;
                        curr = test;
                    }
                }
            }
        }
        if (best_curr_score > best_val) {
            best_val = best_curr_score;
            best_poly = curr;
        }
    }
    
    best_m = 0;
    best_s = 0;
    for (const auto& f : fish_data) {
        Point p = {f.x, f.y};
        int min_x = min(best_poly[0].x, min(best_poly[1].x, min(best_poly[2].x, best_poly[3].x)));
        int max_x = max(best_poly[0].x, max(best_poly[1].x, max(best_poly[2].x, best_poly[3].x)));
        int min_y = min(best_poly[0].y, min(best_poly[1].y, min(best_poly[2].y, best_poly[3].y)));
        int max_y = max(best_poly[0].y, max(best_poly[1].y, max(best_poly[2].y, best_poly[3].y)));
        if (p.x >= min_x && p.x <= max_x && p.y >= min_y && p.y <= max_y) {
            if (f.type == 1) best_m++;
            else best_s++;
        }
    }
    
    return best_poly;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    cin >> N;
    fish_data.resize(2 * N);
    for (int i = 0; i < N; i++) {
        cin >> fish_data[i].x >> fish_data[i].y;
        fish_data[i].type = 1;
    }
    for (int i = 0; i < N; i++) {
        cin >> fish_data[N + i].x >> fish_data[N + i].y;
        fish_data[N + i].type = -1;
    }
    
    build_grid();
    
    // Find best cell as seed
    int best_r = 0, best_c = 0, best_score = -1e9;
    for (int r = 0; r < GRID_SIZE; r++) {
        for (int c = 0; c < GRID_SIZE; c++) {
            if (grid_score[r][c] > best_score) {
                best_score = grid_score[r][c];
                best_r = r;
                best_c = c;
            }
        }
    }
    
    int best_m = 0, best_s = 0;
    int best_val = -1e9;
    vector<Point> best_poly;
    
    mt19937 rng(42);
    uniform_int_distribution<> dist(-2000, 2000);
    
    // Run more restarts from the best cell and nearby cells
    for (int restart = 0; restart < 30; restart++) {
        int pert_x = dist(rng);
        int pert_y = dist(rng);
        int seed_x = best_c * CELL_SIZE + pert_x;
        int seed_y = best_r * CELL_SIZE + pert_y;
        seed_x = max(0, min(MAX_COORD_VAL, seed_x));
        seed_y = max(0, min(MAX_COORD_VAL, seed_y));
        
        int seed_r = seed_y / CELL_SIZE;
        int seed_c = seed_x / CELL_SIZE;
        
        vector<Point> poly = build_poly_from_seeds(seed_r, seed_c);
        if (!is_valid(poly)) continue;
        
        poly = hill_climb(poly, best_m, best_s);
        if (!is_valid(poly)) continue;
        
        long long score = calc_score(poly);
        if (score > best_val) {
            best_val = score;
            best_poly = poly;
        }
    }
    
    cout << best_poly.size() << "\\n";
    for (const auto& p : best_poly) {
        cout << p.x << " " << p.y << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
