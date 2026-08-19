# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(0);cin.tie(0);
    int N;cin>>N;
    vector<pair<int,int>>M(N),S(N);
    for(int i=0;i<N;i++)cin>>M[i].first>>M[i].second;
    for(int i=0;i<N;i++)cin>>S[i].first>>S[i].second;
    vector<pair<int,int>>ans={{0,0},{100000,0},{100000,100000},{0,100000}};
    auto in=[&](pair<int,int>p,int x1,int y1,int x2,int y2){
        return p.first>=x1&&p.first<=x2&&p.second>=y1&&p.second<=y2;
    };
    int best=-1e9;
    for(int r=0;r<15;r++){
        vector<vector<int>>cl;
        vector<bool>vis(N,0);
        for(int i=0;i<N;i++){
            if(vis[i])continue;
            vector<int>c;queue<int>q;
            q.push(i);vis[i]=1;c.push_back(i);
            while(q.size()){
                int u=q.front();q.pop();
                for(int v=0;v<N;v++){
                    if(vis[v])continue;
                    int dx=M[u].first-M[v].first,dy=M[u].second-M[v].second;
                    if(dx*dx+dy*dy<40000){vis[v]=1;q.push(v);c.push_back(v);}
                }
            }
            if(c.size()>=3)cl.push_back(c);
        }
        for(auto&c:cl){
            int mnX=200000,mxX=0,mnY=200000,mxY=0;
            for(int x:c){mnX=min(mnX,M[x].first);mxX=max(mxX,M[x].first);mnY=min(mnY,M[x].second);mxY=max(mxY,M[x].second);}
            int lx=max(0,mnX-50),rx=min(100000,mxX+50),ly=max(0,mnY-50),ry=min(100000,mxY+50);
            int m=0,s=0;
            for(auto&f:M)if(in(f,lx,ly,rx,ry))m++;
            for(auto&f:S)if(in(f,lx,ly,rx,ry))s++;
            if(m-s>best){best=m-s;ans={{lx,ly},{rx,ly},{rx,ry},{lx,ry}};}
            for(int sh=5;sh<=25;sh++){
                for(int d=1;d>=-1;d-=2){
                    int tx=rx+d*sh,ty=ry+d*sh;
                    if(tx<0||tx>100000||ty<0||ty>100000)continue;
                    int cur=0;
                    for(auto&f:M)if(in(f,lx,ly,tx,ty))cur++;
                    for(auto&f:S)if(in(f,lx,ly,tx,ty))cur--;
                    if(cur>best){best=cur;ans={{lx,ly},{rx,ly},{tx,ty},{lx,ty}};}
                    break;
                }
            }
        }
    }
    cout<<"4"<<endl;
    cout<<ans[0].first<<" "<<ans[0].second<<endl;
    cout<<ans[1].first<<" "<<ans[1].second<<endl;
    cout<<ans[2].first<<" "<<ans[2].second<<endl;
    cout<<ans[3].first<<" "<<ans[3].second<<endl;
}
'''
# EVOLVE-BLOCK-END
