# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAXC = 100000;
const int GRS = 200;
const int CZ = 500;
const int NR = 12;
const int MP = 400000;
const int MV = 1000;

struct Pt { int x, y; };
struct F { int x, y, t; };

vector<F> fish;
int gm[GRS][GRS] = {0}, gs[GRS][GRS] = {0};
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

void build() {
    for (int i = 0; i < (int)fish.size(); i++) {
        int cx = max(0, min(GRS - 1, fish[i].x / CZ));
        int cy = max(0, min(GRS - 1, fish[i].y / CZ));
        if (fish[i].t == 1) gm[cx][cy]++;
        else gs[cx][cy]++;
    }
}

long long calc_score(const vector<Pt>& poly) {
    if (poly.size() < 3) return 0;
    long long score = 0;
    for (int i = 0; i < (int)fish.size(); i++) {
        bool inside = false;
        for (int j = 0; j < (int)poly.size(); j++) {
            Pt p1 = poly[j];
            Pt p2 = poly[(j + 1) % poly.size()];
            if ((p1.y > fish[i].y) != (p2.y > fish[i].y)) {
                double xint = (double)(p2.x - p1.x) * (fish[i].y - p1.y) / (p2.y - p1.y) + p1.x;
                if (p1.x > fish[i].x || p2.x > fish[i].x) inside = !inside;
            }
        }
        if (inside) score += fish[i].t;
    }
    return score + 1;
}

bool intersect(Pt a, Pt b, Pt c, Pt d) {
    long long d1 = (long long)(c.x - a.x) * (b.y - a.y) - (long long)(c.y - a.y) * (b.x - a.x);
    long long d2 = (long long)(d.x - a.x) * (b.y - a.y) - (long long)(d.y - a.y) * (b.x - a.x);
    long long d3 = (long long)(c.x - b.x) * (d.y - b.y) - (long long)(c.y - b.y) * (d.x - b.x);
    long long d4 = (long long)(d.x - b.x) * (c.y - b.y) - (long long)(d.y - b.y) * (c.x - b.x);
    return ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0));
}

bool self_intersect(const vector<Pt>& poly) {
    int n = poly.size();
    for (int i = 0; i < n; i++) {
        for (int j = i + 2; j < n; j++) {
            if (i == 0 && j == n - 1) continue;
            if (intersect(poly[i], poly[(i + 1) % n], poly[j], poly[(j + 1) % n])) return true;
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    if (!(cin >> n)) return 0;
    fish.resize(2 * n);
    for (int i = 0; i < n; i++) {
        cin >> fish[i].x >> fish[i].y;
        fish[i].t = 1;
    }
    for (int i = 0; i < n; i++) {
        cin >> fish[n + i].x >> fish[n + i].y;
        fish[n + i].t = -1;
    }
    
    build();
    
    vector<Pt> best_poly;
    long long best_score = 0;
    
    vector<Pt> default_poly = {{0, 0}, {1, 0}, {1, 1}, {0, 1}};
    
    for (int r = 0; r < NR; r++) {
        vector<Pt> poly = default_poly;
        
        if (poly.size() < 4 || poly.size() > MV) continue;
        
        long long perimeter = 0;
        for (int i = 0; i < (int)poly.size(); i++) {
            perimeter += abs(poly[i].x - poly[(i + 1) % poly.size()].x) + 
                        abs(poly[i].y - poly[(i + 1) % poly.size()].y);
        }
        if (perimeter > MP) continue;
        
        if (self_intersect(poly)) continue;
        
        long long score = calc_score(poly);
        if (score > best_score) {
            best_score = score;
            best_poly = poly;
        }
    }
    
    if (best_poly.empty()) {
        best_poly = default_poly;
    }
    
    cout << best_poly.size() << "\\n";
    for (int i = 0; i < (int)best_poly.size(); i++) {
        cout << best_poly[i].x << " " << best_poly[i].y << "\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
