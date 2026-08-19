# EVOLVE-BLOCK-START
CPP_CODE = '''\
#include <bits/stdc++.h>
using namespace std;

const int MAX_COORD = 100000;
const int GRID_SIZE = 200;
const int CELL_SIZE = 500;

struct Point { int x, y; };
vector<Point> mackerels, sardines;

struct Cell { int m=0, s=0; } grid[GRID_SIZE][GRID_SIZE];
vector<Point> good_cells;

int score_rect(int x1, int y1, int x2, int y2) {
    int m=0, s=0;
    for(const auto& f : mackerels) if(f.x>=x1 && f.x<=x2 && f.y>=y1 && f.y<=y2) m++;
    for(const auto& f : sardines) if(f.x>=x1 && f.x<=x2 && f.y>=y1 && f.y<=y2) s++;
    return max(0, m-s+1);
}

vector<Point> make_rect(int cx, int cy, int w, int h) {
    int x1 = max(0, cx-w/2), x2 = min(MAX_COORD, cx+w/2);
    int y1 = max(0, cy-h/2), y2 = min(MAX_COORD, cy+h/2);
    if(x1>=x2 || y1>=y2) return {{0,0},{1,0},{1,1},{0,1}};
    return {{x1,y1},{x2,y1},{x2,y2},{x1,y2}};
}

int main() {
    ios::sync_with_stdio(0);
    int n;
    cin >> n;
    
    mackerels.resize(n);
    sardines.resize(n);
    for(int i=0; i<n; i++) cin >> mackerels[i].x >> mackerels[i].y;
    for(int i=0; i<n; i++) cin >> sardines[i].x >> sardines[i].y;
    
    for(int r=0; r<GRID_SIZE; r++)
        for(int c=0; c<GRID_SIZE; c++) grid[r][c] = {0,0};
    
    for(const auto& f : mackerels) {
        int r = max(0, min(GRID_SIZE-1, f.y/CELL_SIZE));
        int c = max(0, min(GRID_SIZE-1, f.x/CELL_SIZE));
        grid[r][c].m++;
    }
    for(const auto& f : sardines) {
        int r = max(0, min(GRID_SIZE-1, f.y/CELL_SIZE));
        int c = max(0, min(GRID_SIZE-1, f.x/CELL_SIZE));
        grid[r][c].s++;
    }
    
    for(int r=0; r<GRID_SIZE; r++)
        for(int c=0; c<GRID_SIZE; c++)
            if(grid[r][c].m - grid[r][c].s > 0)
                good_cells.push_back({c*CELL_SIZE + CELL_SIZE/2, r*CELL_SIZE + CELL_SIZE/2});
    
    if(good_cells.empty()) {
        vector<Point> poly = {{0,0},{50000,0},{50000,50000},{0,50000}};
        cout << poly.size() << endl;
        for(auto p : poly) cout << p.x << " " << p.y << endl;
        return 0;
    }
    
    vector<Point> best_poly = {{0,0},{50000,0},{50000,50000},{0,50000}};
    int best_score = 0;
    
    int m=0, s=0;
    for(const auto& f : mackerels) if(f.x>=0 && f.x<=50000 && f.y>=0 && f.y<=50000) m++;
    for(const auto& f : sardines) if(f.x>=0 && f.x<=50000 && f.y>=0 && f.y<=50000) s++;
    best_score = max(0, m-s+1);
    
    srand(123);
    
    int min_mx = MAX_COORD, max_mx = 0, min_my = MAX_COORD, max_my = 0;
    for(const auto& f : mackerels) {
        min_mx = min(min_mx, f.x); max_mx = max(max_mx, f.x);
        min_my = min(min_my, f.y); max_my = max(max_my, f.y);
    }
    
    int cx = (min_mx + max_mx) / 2, cy = (min_my + max_my) / 2;
    for(int w : {100,200,400,800,1600,3200,6400}) {
        for(int h : {100,200,400,800,1600,3200,6400}) {
            vector<Point> poly = make_rect(cx, cy, w, h);
            int x1=poly[0].x, x2=poly[1].x, y1=poly[0].y, y2=poly[1].y;
            int sc = score_rect(x1, y1, x2, y2);
            if(sc > best_score) {
                best_score = sc;
                best_poly = poly;
            }
        }
    }
    
    for(int sx : {min_mx, max_mx}) {
        for(int sy : {min_my, max_my}) {
            for(int w : {40000, 60000, 80000, 100000}) {
                for(int h : {40000, 60000, 80000, 100000}) {
                    vector<Point> poly = make_rect(sx, sy, w, h);
                    int x1=poly[0].x, x2=poly[1].x, y1=poly[0].y, y2=poly[1].y;
                    int sc = score_rect(x1, y1, x2, y2);
                    if(sc > best_score) {
                        best_score = sc;
                        best_poly = poly;
                    }
                }
            }
        }
    }
    
    int best_m_s = INT_MIN, best_gi = 0;
    for(int i=0; i<good_cells.size(); i++) {
        int d = grid[good_cells[i].y/CELL_SIZE][good_cells[i].x/CELL_SIZE].m - grid[good_cells[i].y/CELL_SIZE][good_cells[i].x/CELL_SIZE].s;
        if(d > best_m_s) {
            best_m_s = d;
            best_gi = i;
        }
    }
    
    for(int w : {300,600,1200,2400,4800,9600,19200}) {
        for(int h : {300,600,1200,2400,4800,9600,19200}) {
            vector<Point> poly = make_rect(good_cells[best_gi].x, good_cells[best_gi].y, w, h);
            int x1=poly[0].x, x2=poly[1].x, y1=poly[0].y, y2=poly[1].y;
            int sc = score_rect(x1, y1, x2, y2);
            if(sc > best_score) {
                best_score = sc;
                best_poly = poly;
            }
        }
    }
    
    cout << best_poly.size() << endl;
    for(const auto& p : best_poly) cout << p.x << " " << p.y << endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
