# EVOLVE-BLOCK-START
CPP_CODE = r'''#include <bits/stdc++.h>
using namespace std;
int main(){
    int N;cin>>N;
    struct S{int x,y;};
    vector<S>m(N),s(N);
    for(int i=0;i<N;++i){cin>>m[i].x>>m[i].y;}
    for(int i=0;i<N;++i){cin>>s[i].x>>s[i].y;}
    vector<S>best={{0,0},{10000,0},{10000,10000},{0,10000}};int bestv=0;
    auto inP=[&](const vector<S>&poly,int fx,int fy){int w=0;for(size_t i=0;i<poly.size();++i){auto a=poly[i],b=poly[(i+1)%poly.size()];bool ay=a.y>fy,by=b.y>fy;if(ay^by){double t=(fy-a.y)/((double)(b.y-a.y));if(fx<a.x+t*(b.x-a.x))w++;}}return w%2;};
    auto cm=[&](const vector<S>&p){int c=0;for(int i=0;i<N;++i)if(inP(p,m[i].x,m[i].y))c++;return c;};
    auto cs=[&](const vector<S>&p){int c=0;for(int i=0;i<N;++i)if(inP(p,s[i].x,s[i].y))c++;return c;};
    auto sc=[&](const vector<S>&p){return max(0,cm(p)-cs(p)+1);};
    auto ok=[&](const vector<S>&p){if(p.empty()||p.size()<4||p.size()>1000)return false;long long pr=0;for(size_t i=0;i<p.size();++i){auto a=p[i],b=p[(i+1)%p.size()];if(a.x!=b.x&&a.y!=b.y)return false;pr+=abs(a.x-b.x)+abs(a.y-b.y);}if(pr>400000)return false;for(auto&v:p)if(v.x<0||v.x>100000||v.y<0||v.y>100000)return false;for(size_t i=0;i<p.size();++i)for(size_t j=i+1;j<p.size();++j)if(p[i].x==p[j].x&&p[i].y==p[j].y)return false;return true;};
    S gm=m[0],gp=m[0];for(auto&x:m){gm.x=min(gm.x,x.x);gm.y=min(gm.y,x.y);gp.x=max(gp.x,x.x);gp.y=max(gp.y,x.y);}
    S gm2=gm,gp2=gp;int ma=200;for(auto&x:s){if(x.x<=gm2.x+ma)gm2.x=max(0,gm2.x);if(x.x>=gp2.x-ma)gp2.x=min(100000,gp2.x);if(x.y<=gm2.y+ma)gm2.y=max(0,gm2.y);if(x.y>=gp2.y-ma)gp2.y=min(100000,gp2.y);}
    long long cx=0,cy=0;for(auto&x:m){cx+=x.x;cy+=x.y;}cx/=N;cy/=N;
    vector<vector<S>>cands;
    // Tight bbox
    {vector<S>r;{r.push_back({gm2.x,gm2.y});r.push_back({gp2.x,gm2.y});r.push_back({gp2.x,gp2.y});r.push_back({gm2.x,gp2.y});cands.push_back(r);}}
    // Various centroid squares
    for(int sz=50;sz<=1200;sz+=50){
        vector<S>c;
        c.push_back({max(0,(int)cx-sz),max(0,(int)cy-sz)});
        c.push_back({min(100000,(int)cx+sz),max(0,(int)cy-sz)});
        c.push_back({min(100000,(int)cx+sz),min(100000,(int)cy+sz)});
        c.push_back({max(0,(int)cx-sz),min(100000,(int)cy+sz)});
        cands.push_back(c);
    }
    // Offset centroid squares (center shifted)
    for(int ox=-300;ox<=300;ox+=100){
        for(int oy=-300;oy<=300;oy+=100){
            if(ox==0&&oy==0)continue;
            vector<S>c;
            c.push_back({max(0,(int)(cx+ox)-200),max(0,(int)(cy+oy)-200)});
            c.push_back({min(100000,(int)(cx+ox)+200),max(0,(int)(cy+oy)-200)});
            c.push_back({min(100000,(int)(cx+ox)+200),min(100000,(int)(cy+oy)+200)});
            c.push_back({max(0,(int)(cx+ox)-200),min(100000,(int)(cy+oy)+200)});
            cands.push_back(c);
        }
    }
    for(auto&x:cands){if(!ok(x))continue;for(int it=0;it<5;++it){bool imp=false;for(size_t i=0;i<x.size()&&i<150;++i){for(int dx=-30;dx<=30;dx+=5){for(int dy=-30;dy<=30;dy+=5){vector<S>nxt=x;int nx=x[i].x+dx,ny=x[i].y+dy;if(nx<0||nx>100000||ny<0||ny>100000)continue;auto vn=nxt[(i+1)%nxt.size()];if(x[i].x!=vn.x&&x[i].y!=vn.y)continue;nxt[i]={nx,ny};if(ok(nxt)){if(sc(nxt)>sc(x)){x=nxt;imp=true;break;}}}}if(imp)break;}}int v=sc(x);if(v>bestv){bestv=v;best=x;}}if(best.size()==0)best={{0,0},{10000,0},{10000,10000},{0,10000}};cout<<best.size()<<endl;for(auto&x:best)cout<<x.x<<" "<<x.y<<endl;return 0;}
'''
# EVOLVE-BLOCK-END
