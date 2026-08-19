# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAX_C = 100000;
const int G = 200, SZ = 500;
const int MP = 400000;

struct Cell { int m,s; };
Cell grid[G][G];
vector<pair<int,int>> M,N;

void build() {
    for(int i=0;i<G;++i)
        for(int j=0;j<G;++j){
            int m=0,s=0;
            for(auto&p:M) if(p.first/SZ==j&&p.second/SZ==i)m++;
            for(auto&p:N) if(p.first/SZ==j&&p.second/SZ==i)s++;
            grid[i][j]={m,s};
        }
}

int qr(int x1,int y1,int x2,int y2){
    if(x1>x2)swap(x1,x2);if(y1>y2)swap(y1,y2);
    int r1=x1/SZ,r2=x2/SZ,c1=y1/SZ,c2=y2/SZ;
    int m=0,s=0;
    for(int i=r1;i<=r2;++i)
        for(int j=c1;j<=c2;++j){m+=grid[i][j].m;s+=grid[i][j].s;}
    return m-s;
}

int cnt(const vector<pair<int,int>>&p){
    if(p.size()<4)return 0;
    int ans=0;
    for(size_t i=0;i<p.size();++i){
        auto a=p[i],b=p[(i+1)%p.size()];
        ans+=qr(max(0,a.first),max(0,a.second),min(MAX_C,b.first),min(MAX_C,b.second));
    }
    return ans;
}

long long pe(const vector<pair<int,int>>&p){
    long long x=0;
    for(size_t i=0;i<p.size();++i){
        auto a=p[i],b=p[(i+1)%p.size()];
        x+=abs(a.first-b.first)+abs(a.second-b.second);
    }
    return x;
}

bool ok(const vector<pair<int,int>>&p){
    if(p.size()<4||pe(p)>MP)return 0;
    int n=p.size();
    for(int i=0;i<n;++i){
        auto a=p[i],b=p[(i+1)%n];
        if(a.first!=b.first&&a.second!=b.second)return 0;
        if(a.first==b.first&&a.second==b.second)return 0;
        if(a.first<0||a.first>MAX_C||a.second<0||a.second>MAX_C)return 0;
    }
    if(n<4)return 0;
    for(int i=0;i<n;++i){
        for(int j=i+2;j<n;++j){
            if(i==0&&j==n-1)continue;
            auto a=p[i],b=p[(i+1)%n],c=p[j],d=p[(j+1)%n];
            long long cp1=(long long)(b.first-a.first)*(c.second-a.second)-(long long)(b.second-a.second)*(c.first-a.first);
            long long cp2=(long long)(b.first-a.first)*(d.second-a.second)-(long long)(b.second-a.second)*(d.first-a.first);
            if(((cp1>0&&cp2<0)||(cp1<0&&cp2>0))&&((long long)(d.first-c.first)*(a.second-c.second)-(long long)(d.second-c.second)*(a.first-c.first)>0))
                return 0;
        }
    }
    return 1;
}

int main(){
    int Nf;cin>>Nf;
    M.resize(Nf);N.resize(Nf);
    for(auto&p:M)cin>>p.first>>p.second;
    for(auto&p:N)cin>>p.first>>p.second;
    build();
    
    vector<tuple<int,int,int,int,int>>cells;
    for(int i=0;i<G;++i)for(int j=0;j<G;++j)cells.push_back({i,j,grid[i][j].m-grid[i][j].s,grid[i][j].m,grid[i][j].s});
    sort(cells.begin(),cells.end(),[](auto&a,auto&b){return get<2>(a)>get<2>(b);});
    int k=min(15,(int)cells.size());
    
    vector<pair<int,int>>best;int bestsc=-1e9;
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    
    // 15 restarts with hill climbing - fast and effective
    for(int r=0;r<15;++r){
        int idx=rng()%k;
        auto&cell=cells[idx];
        vector<pair<int,int>>p;
        int x1=get<0>(cell)*SZ,y1=get<1>(cell)*SZ;
        int x2=(get<0>(cell)+1)*SZ-1,y2=(get<1>(cell)+1)*SZ-1;
        p={{x1,y1},{x2,y1},{x2,y2},{x1,y2}};
        
        // Hill climb with optimized shifts
        for(int tt=0;tt<3;++tt){
            bool im=1;
            while(im){im=0;
                for(size_t e=0;e<p.size();++e){
                    auto a=p[e],b=p[(e+1)%p.size()];
                    for(int sh=-25;sh<=25;sh+=5){
                        if(sh==0)continue;
                        vector<pair<int,int>>np=p;
                        if(a.first==b.first){int nx=a.first+sh;if(nx>=0&&nx<=MAX_C){np[e]={nx,a.second};np[(e+1)%p.size()]={nx,b.second};}}
                        else{int ny=a.second+sh;if(ny>=0&&ny<=MAX_C){np[e]={a.first,ny};np[(e+1)%p.size()]={b.first,ny};}}
                        if(ok(np)){int sc=cnt(np);if(sc>bestsc){bestsc=sc;best=np;im=1;}}
                    }
                }
            }
        }
    }
    
    // Fallback - scan only top cells
    if(best.size()<4){
        for(int i=0;i<k;++i){
            int idx=rng()%k;
            auto&cell=cells[idx];
            int x1=get<0>(cell)*SZ,y1=get<1>(cell)*SZ;
            int x2=(get<0>(cell)+1)*SZ-1,y2=(get<1>(cell)+1)*SZ-1;
            vector<pair<int,int>>p={{x1,y1},{x2,y1},{x2,y2},{x1,y2}};
            if(ok(p)){int sc=cnt(p);if(sc>bestsc){bestsc=sc;best=p;}}
        }
    }
    
    if(best.size()<4)best={{0,0},{500,0},{500,500},{0,500}};
    cout<<best.size()<<endl;
    for(auto&p:best)cout<<p.first<<" "<<p.second<<endl;
}
'''
# EVOLVE-BLOCK-END
