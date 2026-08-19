# EVOLVE-BLOCK-START
CPP_CODE = r'''
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <random>
#include <utility>

using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    
    int N;
    cin >> N;
    
    vector<pair<int,int>> mack(N), sard(N);
    for(int i=0;i<N;i++) cin>>mack[i].first>>mack[i].second;
    for(int i=0;i<N;i++) cin>>sard[i].first>>sard[i].second;
    
    // Simple bounding box approach
    int min_x=100000,min_y=100000,max_x=0,max_y=0;
    for(auto&p:mack){min_x=min(min_x,p.first);min_y=min(min_y,p.second);max_x=max(max_x,p.first);max_y=max(max_y,p.second);}
    for(auto&p:sard){min_x=min(min_x,p.first);min_y=min(min_y,p.second);max_x=max(max_x,p.first);max_y=max(max_y,p.second);}
    
    // Count mackerels and sardines in bounding box
    int m_count=0,s_count=0;
    for(auto&p:mack){if(p.first>=min_x&&p.first<=max_x&&p.second>=min_y&&p.second<=max_y)m_count++;}
    for(auto&p:sard){if(p.first>=min_x&&p.first<=max_x&&p.second>=min_y&&p.second<=max_y)s_count++;}
    
    long long best_sc = max(0LL, (long long)m_count - s_count + 1);
    vector<pair<int,int>> best = {{min_x,min_y},{max_x,min_y},{max_x,max_y},{min_x,max_y}};
    
    // Try shrinking from each corner
    mt19937 rng(42);
    
    for(int restart=0;restart<15;restart++){
        int rx=min_x+uniform_int_distribution<int>(0,50)(rng),ry=min_y+uniform_int_distribution<int>(0,50)(rng),
            Rmax_x=max_x-uniform_int_distribution<int>(0,50)(rng),Rmax_y=max_y-uniform_int_distribution<int>(0,50)(rng);
        
        rx=max(0,rx);ry=max(0,ry);Rmax_x=min(100000,Rmax_x);Rmax_y=min(100000,Rmax_y);
        if(rx>Rmax_x||ry>Rmax_y)continue;
        
        int cm=0,cs=0;
        for(auto&p:mack){if(p.first>=rx&&p.first<=Rmax_x&&p.second>=ry&&p.second<=Rmax_y)cm++;}
        for(auto&p:sard){if(p.first>=rx&&p.first<=Rmax_x&&p.second>=ry&&p.second<=Rmax_y)cs++;}
        
        long long sc = max(0LL, (long long)cm - cs + 1);
        if(sc>best_sc){
            best_sc=sc;
            best={{rx,ry},{Rmax_x,ry},{Rmax_x,Rmax_y},{rx,Rmax_y}};
        }
    }
    
    cout<<best.size()<<endl;
    for(auto&p:best)cout<<p.first<<" "<<p.second<<endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
