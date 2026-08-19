# EVOLVE-BLOCK-START
CPP_CODE = '''\
#include <bits/stdc++.h>
using namespace std;
const int MAXC = 100000;
struct Pt { int x,y; };
struct Fish { Pt p; int t; };
vector<Fish> fish;

int main(){
    ios::sync_with_stdio(0);cin.tie(0);
    int N;cin>>N;
    fish.resize(2*N);
    for(int i=0;i<N;i++){cin>>fish[i].p.x>>fish[i].p.y;fish[i].t=1;}
    for(int i=0;i<N;i++){cin>>fish[N+i].p.x>>fish[N+i].p.y;fish[N+i].t=-1;}
    
    vector<Pt>best={{0,0},{1,0},{1,1},{0,1}};
    
    int mx=MAXC,my=MAXC,MX=0,MY=0;
    for(auto&f:fish){mx=min(mx,f.p.x);my=min(my,f.p.y);MX=max(MX,f.p.x);MY=max(MY,f.p.y);}
    
    for(int r=0;r<20;r++){
        vector<Pt>init={{mx,my},{MX,my},{MX,MY},{mx,MY}};
        vector<Pt>P=init;
        int bm=0,bs=0;
        for(auto&f:fish){
            int wn=0;
            for(size_t i=0;i<P.size();i++){
                Pt a=P[i],b=P[(i+1)%P.size()];
                if(a.y<=f.p.y){
                    if(b.y>f.p.y&&(long long)(b.x-a.x)*(f.p.y-a.y)>(long long)(f.p.x-a.x)*(b.y-a.y))wn++;
                }else{
                    if(b.y<=f.p.y&&(long long)(b.x-a.x)*(f.p.y-a.y)<(long long)(f.p.x-a.x)*(b.y-a.y))wn--;
                }
            }
            if(wn!=0)if(f.t==1)bm++;else bs++;
        }
        for(int hc=0;hc<80;hc++){bool ok=false;
            for(size_t v=0;v<P.size();v++){Pt o=P[v];
                for(int s=1;s<=15;s++){for(int d=-1;d<=1;d++){if(d==0)continue;
                    int nx=P[v].x+d*s,ny=P[v].y+d*s;
                    if(nx<0||nx>MAXC||ny<0||ny>MAXC)continue;
                    P[v]={nx,ny};
                    int d0=0,d1=0;
                    for(auto&f:fish){
                        int wn=0;
                        for(size_t i=0;i<P.size();i++){
                            Pt a=P[i],b=P[(i+1)%P.size()];
                            if(a.y<=f.p.y){
                                if(b.y>f.p.y&&(long long)(b.x-a.x)*(f.p.y-a.y)>(long long)(f.p.x-a.x)*(b.y-a.y))wn++;
                            }else{
                                if(b.y<=f.p.y&&(long long)(b.x-a.x)*(f.p.y-a.y)<(long long)(f.p.x-a.x)*(b.y-a.y))wn--;
                            }
                        }
                        if(wn!=0)if(f.t==1)d0++;else d1++;
                    }
                    if(d0-d1>0){ok=true;break;}P[v]=o;
                }if(ok)break;}
            }if(!ok)break;}
        if(max(0,bm-bs+1)>max(0,best.size()==0?0:1)){best=P;}
    }
    
    cout<<best.size()<<endl;
    for(auto&p:best)cout<<p.x<<" "<<p.y<<endl;
    return 0;
}
'''
# EVOLVE-BLOCK-END
