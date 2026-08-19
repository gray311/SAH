# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAX_COORD = 100000;

struct Pt { int x, y; };

vector<Pt> mack, sard;

vector<Pt> make_rect(int x, int y, int w, int h) {
    return {{x,y},{x+w,y},{x+w,y+h},{x,y+h}};
}

vector<Pt> make_l(int x, int y, int w, int h, int cx, int cy, int cw, int ch) {
    return {{x,y},{x+w,y},{x+w,cy},{x+w-cw,cy},{x+w-cw,cy+ch},{x+w,cy+ch},{x+w,y+h},{x,y+h},{x,cy+ch},{x,cy}};
}

bool valid(const vector<Pt>& p) {
    if (p.size() < 4 || p.size() > 1000) return false;
    long long per = 0;
    for (int i = 0; i < (int)p.size(); i++) {
        per += abs(p[i].x - p[(i+1)%p.size()].x) + abs(p[i].y - p[(i+1)%p.size()].y);
        if (per > 400000) return false;
    }
    for (int i = 0; i < (int)p.size(); i++) {
        if (p[i].x != p[(i+1)%p.size()].x && p[i].y != p[(i+1)%p.size()].y) return false;
        if (p[i].x == p[(i+1)%p.size()].x && p[i].y == p[(i+1)%p.size()].y) return false;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int N;
    if (!(cin >> N)) {
        cout << "4\\n0 0\\n100 0\\n100 100\\n0 100\\n";
        return 0;
    }
    
    mack.resize(N);
    sard.resize(N);
    
    for (int i = 0; i < N; i++) cin >> mack[i].x >> mack[i].y;
    for (int i = 0; i < N; i++) cin >> sard[i].x >> sard[i].y;
    
    int mx = MAX_COORD, my = MAX_COORD, Mx = 0, My = 0;
    for (auto& f : mack) { mx = min(mx, f.x); Mx = max(Mx, f.x); my = min(my, f.y); My = max(My, f.y); }
    for (auto& f : sard) { mx = min(mx, f.x); Mx = max(Mx, f.x); my = min(my, f.y); My = max(My, f.y); }
    
    mx = max(0, mx - 50); Mx = min(MAX_COORD, Mx + 50);
    my = max(0, my - 50); My = min(MAX_COORD, My + 50);
    
    vector<vector<Pt>> cands;
    
    int gs = 400;
    map<pair<int,int>, int> gm, gs_map;
    for (auto& f : mack) gm[{f.x/gs, f.y/gs}]++;
    for (auto& f : sard) gs_map[{f.x/gs, f.y/gs}]++;
    
    // Dense mackerel regions
    for (auto& kv : gm) {
        if (kv.second < 2) continue;
        int gx = kv.first.first * gs, gy = kv.first.second * gs;
        for (int s = 100; s <= 2000; s += 100) {
            int x = max(0, gx - s/2), y = max(0, gy - s/2);
            int w = min(MAX_COORD - x, s), h = min(MAX_COORD - y, s);
            if (w > 0 && h > 0) cands.push_back(make_rect(x, y, w, h));
        }
    }
    
    // L-shapes to avoid sardine clusters
    for (auto& kv : gm) {
        if (kv.second < 3) continue;
        int gx = kv.first.first * gs, gy = kv.first.second * gs;
        int x = max(0, gx - 800), y = max(0, gy - 800);
        int w = min(MAX_COORD - x, 1800), h = min(MAX_COORD - y, 1800);
        if (w <= 0 || h <= 0) continue;
        
        for (auto& skv : gs_map) {
            if (skv.second < 2) continue;
            int sx = skv.first.first * gs, sy = skv.first.second * gs;
            int cx = max(x, sx - 300), cy = max(y, sy - 300);
            int cw = min(w - cx, 600), ch = min(h - cy, 600);
            if (cw > 0 && ch > 0) cands.push_back(make_l(x, y, w, h, cx, cy, cw, ch));
        }
    }
    
    // Corner rectangles
    int sz[] = {300, 600, 1000, 1400, 1800};
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int s : sz) {
                int x = (i == 0) ? 0 : Mx - 50;
                int y = (j == 0) ? 0 : My - 50;
                int w = min(MAX_COORD - x, s), h = min(MAX_COORD - y, s);
                if (w > 0 && h > 0) cands.push_back(make_rect(x, y, w, h));
            }
        }
    }
    
    mt19937 rng(42);
    for (int i = 0; i < 300; i++) {
        int x = rng() % (Mx - mx + 1) + mx;
        int y = rng() % (My - my + 1) + my;
        int w = 200 + rng() % 1200;
        int h = 200 + rng() % 1200;
        if (x + w <= MAX_COORD && y + h <= MAX_COORD) cands.push_back(make_rect(x, y, w, h));
    }
    
    // Score and pick best
    vector<pair<int, vector<Pt>>> scored;
    for (auto& poly : cands) {
        if (!valid(poly)) continue;
        int mc = 0, sc = 0;
        for (auto& f : mack) {
            int wn = 0;
            for (int j = 0; j < (int)poly.size(); j++) {
                Pt a = poly[j], b = poly[(j+1)%poly.size()];
                if (a.y <= f.y && b.y > f.y && (long long)(b.x - a.x) * (f.y - a.y) > 0 && b.x > f.x) wn++;
            }
            if (wn) mc++;
        }
        for (auto& f : sard) {
            int wn = 0;
            for (int j = 0; j < (int)poly.size(); j++) {
                Pt a = poly[j], b = poly[(j+1)%poly.size()];
                if (a.y <= f.y && b.y > f.y && (long long)(b.x - a.x) * (f.y - a.y) > 0 && b.x > f.x) wn++;
            }
            if (wn) sc++;
        }
        scored.push_back({max(0, mc - sc + 1), poly});
    }
    
    sort(scored.begin(), scored.end(), [](auto& a, auto& b) { return a.first > b.first; });
    
    if (!scored.empty()) {
        cout << scored[0].second.size() << "\\n";
        for (auto& p : scored[0].second) cout << p.x << " " << p.y << "\\n";
    } else {
        cout << "4\\n0 0\\n100 0\\n100 100\\n0 100\\n";
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
