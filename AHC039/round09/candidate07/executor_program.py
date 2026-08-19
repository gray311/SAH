# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>

using namespace std;

const int MAX_COORD = 100000;
const int GRID_SIZE = 500;
const int CELL_SIZE = 200;

struct Point { int x,y; };
struct Cell { int M=0,S=0; int v(){return M-S;} };
Cell grid[GRID_SIZE][GRID_SIZE];
vector<Point> fish[2];
int N;

int rect_score(int x1,int y1,int x2,int y2){
    if(x1>x2||y1>y2)return 0;
    int m=0,s=0;
    for(int i=0;i<N;i++){
        if(fish[0][i].x>=x1 && fish[0][i].x<=x2 && fish[0][i].y>=y1 && fish[0][i].y<=y2) m++;
        if(fish[1][i].x>=x1 && fish[1][i].x<=x2 && fish[1][i].y>=y1 && fish[1][i].y<=y2) s++;
    }
    return m-s+1;
}

int main(){
    ios::sync_with_stdio(0);
    cin.tie(0);
    if(!(cin>>N)) return 0;
    fish[0].resize(N);
    for(int i=0;i<N;i++) cin>>fish[0][i].x>>fish[0][i].y;
    fish[1].resize(N);
    for(int i=0;i<N;i++) cin>>fish[1][i].x>>fish[1][i].y;
    
    for(int i=0;i<N;i++){
        int r=fish[0][i].y/CELL_SIZE,c=fish[0][i].x/CELL_SIZE;
        if(r>=0&&r<GRID_SIZE&&c>=0&&c<GRID_SIZE) grid[r][c].M++;
        r=fish[1][i].y/CELL_SIZE,c=fish[1][i].x/CELL_SIZE;
        if(r>=0&&r<GRID_SIZE&&c>=0&&c<GRID_SIZE) grid[r][c].S++;
    }
    
    vector<Point> best={{0,0},{1,0},{1,1},{0,1}};
    int best_sc=rect_score(0,0,1,1);
    
    // Collect all cells that are sardine-safe (S <= M + 2)
    vector<pair<int,int>> safe_cells;
    for(int i=0;i<GRID_SIZE;i++)
        for(int j=0;j<GRID_SIZE;j++)
            if(grid[i][j].S <= grid[i][j].M + 2)
                safe_cells.push_back({i,j});
    
    random_device rd;mt19937 g(rd());
    
    // Try 25 random safe cells
    for(int r=0;r<25 && !safe_cells.empty();r++){
        int idx = g() % safe_cells.size();
        int i=safe_cells[idx].first,j=safe_cells[idx].second;
        
        // Start with cell-sized rectangle
        int x1=i*CELL_SIZE,y1=i*CELL_SIZE;
        int x2=(j+1)*CELL_SIZE,y2=(i+1)*CELL_SIZE;
        
        // Expand while safe
        for(int dir=0;dir<2;dir++){ // expand right and down
            for(int k=0;k<20 && x2+200<=MAX_COORD;k++){
                int next_c = j + dir*2;
                if(next_c>=GRID_SIZE) break;
                if(grid[i][next_c].S <= grid[i][next_c].M + 2){
                    x2 = (next_c+1)*CELL_SIZE;
                } else break;
            }
        }
        
        // Hill climb on this rectangle
        for(int sh=2;sh<=25;sh+=2)
            for(int dx=-sh;dx<=sh;dx+=2)
                for(int dy=-sh;dy<=sh;dy+=2){
                    int nx1=x1+dx,ny1=y1+dy;
                    int nx2=x2+dx,ny2=y2+dy;
                    if(nx1>=0&&nx2<=MAX_COORD&&ny1>=0&&ny2<=MAX_COORD&&nx1<=nx2&&ny1<=ny2){
                        int sc=rect_score(nx1,ny1,nx2,ny2);
                        if(sc>best_sc){
                            best_sc=sc;
                            best={{nx1,ny1},{nx2,ny1},{nx2,ny2},{nx1,ny2}};
                        }
                    }
                }
    }
    
    cout<<best.size()<<endl;
    for(auto&p:best) cout<<p.x<<" "<<p.y<<endl;
    return 0;
}
'''
# EVOLVE-BLOCK-END
