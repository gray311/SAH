# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Point { int x, y; };

bool pointInPoly(Point p, const vector<Point>& poly) {
    int n = poly.size();
    if (n < 4) return false;
    bool inside = false;
    for (int i = 0, j = n - 1; i < n; j = i++) {
        bool vi = poly[i].y > p.y;
        bool vj = poly[j].y > p.y;
        if (vi != vj) {
            double xint = (double)(poly[j].x - poly[i].x) * (double)(p.y - poly[i].y) / (double)(poly[j].y - poly[i].y) + (double)poly[i].x;
            if (p.x < xint) inside = !inside;
        }
    }
    return inside;
}

int main() {
    int N;
    if (!(cin >> N)) return 0;
    
    vector<Point> M(N), S(N);
    for (int i = 0; i < N; i++) cin >> M[i].x >> M[i].y;
    for (int i = 0; i < N; i++) cin >> S[i].x >> S[i].y;
    
    int lx = 200000, rx = -200000, ly = 200000, ry = -200000;
    for (int i = 0; i < N; i++) {
        lx = min(lx, M[i].x); rx = max(rx, M[i].x);
        ly = min(ly, M[i].y); ry = max(ry, M[i].y);
    }
    if (lx > rx || ly > ry) { lx = 0; rx = 100000; ly = 0; ry = 100000; }
    
    vector<Point> best_poly;
    int best_score_val = -1e9;
    
    // Very wide search with various step sizes
    int range = 1000;
    vector<int> steps = {20, 40, 60, 80, 100};
    
    for (int st : steps) {
        for (int dx = -range; dx <= range; dx += st) {
            for (int dy = -range; dy <= range; dy += st) {
                int xx = max(0, lx + dx), yy = max(0, ly + dy);
                int WW = min(100000, rx + dx), HH = min(100000, ry + dy);
                if (xx >= WW || yy >= HH) continue;
                
                int mc = 0, sc = 0;
                vector<Point> cur = {{xx, yy}, {WW, yy}, {WW, HH}, {xx, HH}};
                for (int i = 0; i < N; i++) if (pointInPoly(M[i], cur)) mc++;
                for (int i = 0; i < N; i++) if (pointInPoly(S[i], cur)) sc++;
                
                int score = mc - sc + 1;
                if (score > best_score_val) {
                    best_score_val = score;
                    best_poly = cur;
                }
            }
        }
    }
    
    // Extreme corners
    int ext = 2000;
    vector<int> dirs = {-100, 100};
    for (int d1 : dirs) {
        for (int d2 : dirs) {
            for (int dd = 500; dd <= ext; dd += 500) {
                int xx = max(0, lx + d1 * dd), yy = max(0, ly + d2 * dd);
                int WW = min(100000, rx + d1 * dd), HH = min(100000, ry + d2 * dd);
                if (xx >= WW || yy >= HH) continue;
                
                int mc = 0, sc = 0;
                vector<Point> cur = {{xx, yy}, {WW, yy}, {WW, HH}, {xx, HH}};
                for (int i = 0; i < N; i++) if (pointInPoly(M[i], cur)) mc++;
                for (int i = 0; i < N; i++) if (pointInPoly(S[i], cur)) sc++;
                
                int score = mc - sc + 1;
                if (score > best_score_val) {
                    best_score_val = score;
                    best_poly = cur;
                }
            }
        }
    }
    
    if (best_poly.empty()) best_poly = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
    
    cout << best_poly.size() << "\\n";
    for (auto& p : best_poly) cout << p.x << " " << p.y << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
