# EVOLVE-BLOCK-START
CPP_CODE = '''#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <chrono>
using namespace std;

const int MAX_COORD = 100000;
const int MAX_PERIMETER = 400000;

struct Point { int x, y; };

bool in_rect(Point p, int x1, int y1, int x2, int y2) {
    return p.x >= x1 && p.x <= x2 && p.y >= y1 && p.y <= y2;
}

void count_in_rect(const vector<Point>& m, const vector<Point>& s, int x1, int y1, int x2, int y2, int& m_cnt, int& s_cnt) {
    m_cnt = s_cnt = 0;
    for (int i = 0; i < (int)m.size(); i++) if (in_rect(m[i], x1, y1, x2, y2)) m_cnt++;
    for (int i = 0; i < (int)s.size(); i++) if (in_rect(s[i], x1, y1, x2, y2)) s_cnt++;
}

mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());
int next_int(int n) { if (n <= 0) return 0; return uniform_int_distribution<int>(0, n-1)(rng); }

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    vector<Point> mackerels(N), sardines(N);
    for (int i = 0; i < N; i++) cin >> mackerels[i].x >> mackerels[i].y;
    for (int i = 0; i < N; i++) cin >> sardines[i].x >> sardines[i].y;
    
    if (N == 0) {
        cout << 4 << endl;
        cout << 0 << " " << 0 << endl;
        cout << 1 << " " << 0 << endl;
        cout << 1 << " " << 1 << endl;
        cout << 0 << " " << 1 << endl;
        return 0;
    }
    
    int min_x = MAX_COORD, max_x = 0, min_y = MAX_COORD, max_y = 0;
    for (int i = 0; i < N; i++) {
        min_x = min(min_x, mackerels[i].x);
        max_x = max(max_x, mackerels[i].x);
        min_y = min(min_y, mackerels[i].y);
        max_y = max(max_y, mackerels[i].y);
    }
    
    // Try different padding values - prioritize smaller
    vector<Point> best_poly;
    int best_m = 0, best_s = 0, best_score = -1;
    
    for (int p : {500, 800, 1000, 1500, 2000}) {
        vector<Point> test_poly;
        test_poly.push_back({max(0, min_x - p), max(0, min_y - p)});
        test_poly.push_back({min(MAX_COORD, max_x + p), max(0, min_y - p)});
        test_poly.push_back({min(MAX_COORD, max_x + p), min(MAX_COORD, max_y + p)});
        test_poly.push_back({max(0, min_x - p), min(MAX_COORD, max_y + p)});
        
        int tm, ts;
        count_in_rect(mackerels, sardines, test_poly[0].x, test_poly[0].y, test_poly[1].x, test_poly[0].y, tm, ts);
        int tsc = max(0, tm - ts + 1);
        if (tsc > best_score) {
            best_score = tsc;
            best_m = tm;
            best_s = ts;
            best_poly = test_poly;
        }
    }
    
    // Local search with diverse directions
    auto start_time = chrono::steady_clock::now();
    vector<Point> current_poly = best_poly;
    int current_m = best_m, current_s = best_s;
    int best_search_score = best_score;
    
    for (int iter = 0; iter < 20000; iter++) {
        auto now = chrono::steady_clock::now();
        if (chrono::duration<double>(now - start_time).count() > 1.8) break;
        
        vector<Point> cand = current_poly;
        int edge = next_int(cand.size());
        Point p1 = cand[edge], p2 = cand[(edge+1)%cand.size()];
        
        // Mix of small and medium steps
        int step;
        if (rand() % 3 == 0) step = 100 + next_int(600);
        else step = 400 + next_int(1000);
        
        // Random direction
        int dir = (rand() % 2 == 0) ? 1 : -1;
        
        if (p1.x == p2.x) {
            int nx = p1.x + dir * step;
            nx = max(0, min(MAX_COORD, nx));
            if (nx == p1.x) continue;
            cand[edge].x = nx;
            cand[(edge+1)%cand.size()].x = nx;
        } else {
            int ny = p1.y + dir * step;
            ny = max(0, min(MAX_COORD, ny));
            if (ny == p1.y) continue;
            cand[edge].y = ny;
            cand[(edge+1)%cand.size()].y = ny;
        }
        
        int cm, cs;
        count_in_rect(mackerels, sardines, cand[0].x, cand[0].y, cand[1].x, cand[0].y, cm, cs);
        int sc = max(0, cm - cs + 1);
        
        if (sc > best_search_score) {
            best_search_score = sc;
            best_m = cm;
            best_s = cs;
            best_poly = cand;
        }
    }
    
    cout << best_poly.size() << endl;
    for (const auto& p : best_poly) {
        cout << p.x << " " << p.y << endl;
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
