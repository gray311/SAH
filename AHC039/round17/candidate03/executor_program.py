# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <numeric>

using namespace std;

const int MAXC = 100000;
const int MAXV = 1000;
const int MAXP = 400000;
const int G = 200;
const int C = MAXC / G;

struct F { int x,y,t; };
vector<F> M,S;
int N;
struct Cell { int m,s,sc; };
Cell Gd[200][200];

bool inside(int px, int py, int x1, int y1, int x2, int y2) {
    return px >= x1 && px <= x2 && py >= y1 && py <= y2;
}

int score_rect(int x1, int y1, int x2, int y2) {
    int m = 0, s = 0;
    for(size_t i=0; i<M.size(); i++) if(inside(M[i].x, M[i].y, x1, y1, x2, y2)) m++;
    for(size_t i=0; i<S.size(); i++) if(inside(S[i].x, S[i].y, x1, y1, x2, y2)) s++;
    return m - s;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cin >> N;
    M.resize(N); S.resize(N);
    for(int i=0;i<N;i++) cin>>M[i].x>>M[i].y;
    for(int i=0;i<N;i++) cin>>S[i].x>>S[i].y;
    
    // Build grid
    for(int i=0;i<G;i++)
        for(int j=0;j<G;j++) Gd[i][j]={0,0,0};
    for(size_t i=0;i<M.size();i++){
        int c=min(G-1,M[i].x/C),r=min(G-1,M[i].y/C);
        Gd[r][c].m++;Gd[r][c].sc++;
    }
    for(size_t i=0;i<S.size();i++){
        int c=min(G-1,S[i].x/C),r=min(G-1,S[i].y/C);
        Gd[r][c].s++;Gd[r][c].sc--;
    }
    
    vector<pair<int,int>> best;
    int bestsc = -1000000000;
    
    // Try many different rectangle sizes and positions
    for(int restart=0;restart<30;restart++){
        // Get top cells
        vector<int> cells(G*G);
        iota(cells.begin(),cells.end(),0);
        nth_element(cells.begin(),cells.begin()+50,cells.end(),
            [](int a,int b){return Gd[a/G][a%G].sc>Gd[b/G][b%G].sc;});
        
        // Try many sizes
        int sizes[] = {25, 50, 75, 100, 125, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000};
        int num_sizes = 17;
        
        for(int t=0;t<50;t++){
            int idx=cells[t],cx=idx%G,cy=idx/G;
            
            // Perturb based on restart
            int dc = (restart % 5 == 0) ? -1 : ((restart % 5 == 1) ? 1 : 0);
            int dr = (restart % 4 == 0) ? -1 : ((restart % 4 == 1) ? 1 : 0);
            cx = max(0, min(G-1, cx + dc));
            cy = max(0, min(G-1, cy + dr));
            
            for(int sz=0;sz<num_sizes;sz++){
                int x1=cx*C-sizes[sz],y1=cy*C-sizes[sz];
                int x2=(cx+1)*C+sizes[sz],y2=(cy+1)*C+sizes[sz];
                x1=max(0,x1);y1=max(0,y1);x2=min(MAXC,x2);y2=min(MAXC,y2);
                if(x1<x2&&y1<y2){
                    int sc2 = score_rect(x1,y1,x2,y2);
                    if(sc2>bestsc){
                        bestsc=sc2;
                        best={{x1,y1},{x2,y1},{x2,y2},{x1,y2}};
                    }
                }
            }
        }
        
        // Try expanding in each direction from top cells
        for(int t=0;t<50;t++){
            int idx=cells[t],cx=idx%G,cy=idx/G;
            
            for(int d=0;d<4;d++){
                int dx=(d==0||d==2)?1:0;
                int dy=(d==1||d==3)?1:0;
                int nx=cx+dx*5,ny=cy+dy*5;
                if(nx>=0&&nx<G&&ny>=0&&ny<G){
                    int minx=min(cx,nx),maxx=max(cx,nx);
                    int miny=min(cy,ny),maxy=max(cy,ny);
                    
                    // Try different expansion sizes
                    for(int esz=50;esz<=1200;esz+=75){
                        int x1=minx*C-esz,y1=miny*C-esz;
                        int x2=(maxx+1)*C+esz,y2=(maxy+1)*C+esz;
                        x1=max(0,x1);y1=max(0,y1);x2=min(MAXC,x2);y2=min(MAXC,y2);
                        if(x1<x2&&y1<y2){
                            int sc2 = score_rect(x1,y1,x2,y2);
                            if(sc2>bestsc){
                                bestsc=sc2;
                                best={{x1,y1},{x2,y1},{x2,y2},{x1,y2}};
                            }
                        }
                    }
                }
            }
        }
    }
    
    cout<<best.size()<<"\n";
    for(size_t i=0;i<best.size();i++) cout<<best[i].first<<" "<<best[i].second<<"\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
