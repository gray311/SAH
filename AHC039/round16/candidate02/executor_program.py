# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <bits/stdc++.h>
using namespace std;

int main() {
    int N;
    cin >> N;
    
    vector<pair<int,int>> mack(N), sard(N);
    for(int i=0;i<N;i++) cin >> mack[i].first >> mack[i].second;
    for(int i=0;i<N;i++) cin >> sard[i].first >> sard[i].second;
    
    int CELL = 500;
    vector<int> cell(40000, 0);
    for(const auto& p : mack) cell[p.first/CELL*200 + p.second/CELL]++;
    for(const auto& p : sard) cell[p.first/CELL*200 + p.second/CELL]--;
    
    int pr[205][205];
    for(int i=0;i<=204;i++)
        for(int j=0;j<=204;j++) pr[i][j]=0;
    
    for(int r=0;r<=200;r++)
        for(int c=0;c<=200;c++) pr[r][c]=cell[r*200+c];
    
    for(int i=1;i<=204;i++) pr[i][0]+=pr[i-1][0];
    for(int j=1;j<=204;j++) pr[0][j]+=pr[0][j-1];
    for(int i=1;i<=204;i++){
        for(int j=1;j<=204;j++){
            pr[i][j]+=pr[i-1][j]+pr[i][j-1]-pr[i-1][j-1];
        }
    }
    
    auto query = [&](int x1, int y1, int x2, int y2) -> int {
        int r1=x1/CELL,r2=(y2-1)/CELL+1;
        int c1=y1/CELL,c2=(x2-1)/CELL+1;
        r1=max(0,min(r1,200));r2=max(0,min(r2,200));
        c1=max(0,min(c1,200));c2=max(0,min(c2,200));
        if(r1>r2||c1>c2)return 0;
        return pr[r2][c2]- (r1>0?pr[r1-1][c2]:0) - (c1>0?pr[r2][c1-1]:0) + ((r1>0&&c1>0)?pr[r1-1][c1-1]:0);
    };
    
    int best_x=0,best_x2=1000,best_y=0,best_y2=1000;
    
    for(int k=0;k<25;k++){
        vector<pair<int,int>> cells;
        for(int r=0;r<=200;r++)
            for(int c=0;c<=200;c++)
                if(pr[r][c]>0)cells.push_back({c*CELL,r*CELL});
        
        if(cells.empty())continue;
        
        int mnX=100000,mxX=0,mnY=100000,mxY=0;
        for(int i=0;i<10&&i<(int)cells.size();i++){
            int r=cells[i].second/CELL;
            int c=cells[i].first/CELL;
            mnX=min(mnX,c*CELL);mxX=max(mxX,(c+1)*CELL-1);
            mnY=min(mnY,r*CELL);mxY=max(mxY,(r+1)*CELL-1);
        }
        
        int bx=mnX,bx2=mxX,by=mnY,by2=mxY;
        int sb=query(bx,by,bx2,by2);
        
        // Expand with larger range
        for(int it=0;it<5;it++){
            for(int d=0;d<4;d++){
                int limit=100;
                if(d==0)limit=100000-bx2;
                else if(d==1)limit=bx;
                else if(d==2)limit=100000-by2;
                else limit=by;
                
                for(int a=10;a<=limit&&a<=200;a++){
                    int bx3=bx2,by3=by2;
                    if(d==0)bx3=bx2+a;
                    else if(d==1)bx=bx-a;
                    else if(d==2)by3=by2+a;
                    else by=by-a;
                    
                    int w=bx3-bx+1,h=by3-by+1;
                    if(w<1||h<1)continue;
                    int p=2*(w+h);
                    if(p>400000)continue;
                    
                    int ss=query(bx,by,bx3,by3);
                    if(ss>sb){sb=ss;bx=bx3;bx2=bx3;by=by3;by2=by3;}
                }
            }
        }
        
        int cur=query(bx,by,bx2,by2);
        if(cur>query(best_x,best_y,best_x2,best_y2)){
            best_x=bx;best_x2=bx2;best_y=by;best_y2=by2;
        }
    }
    
    cout << 4 << "\n";
    cout << best_x << " " << best_y << "\n";
    cout << best_x2 << " " << best_y << "\n";
    cout << best_x2 << " " << best_y2 << "\n";
    cout << best_x << " " << best_y2 << "\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
