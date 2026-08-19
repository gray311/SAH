# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MX = 100000, MV = 1000, MP = 400000;

bool is_inside(const vector<pair<int,int>>& P, int px, int py) {
    if(P.size() < 3) return false;
    int n = P.size(), c = 0;
    for(int i=0; i<n; ++i) {
        int x1=P[i].first, y1=P[i].second, x2=P[(i+1)%n].first, y2=P[(i+1)%n].second;
        if((y1>py)!=(y2>py) && px < (double)(x2-x1)*(py-y1)/(y2-y1)+x1) c++;
    }
    return c%2==1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int N; cin >> N;
    vector<pair<int,int>> mack(2*N), sard(2*N);
    for(int i=0; i<N; ++i) cin >> mack[i].first >> mack[i].second;
    for(int i=0; i<N; ++i) cin >> sard[i].first >> sard[i].second;
    
    // Try multiple starting positions around mackerels
    auto score = [&](const vector<pair<int,int>>& Q) {
        int m=0, s=0;
        for(const auto& p : mack) if(is_inside(Q, p.first, p.second)) m++;
        for(const auto& p : sard) if(is_inside(Q, p.first, p.second)) s++;
        return m - s;
    };
    
    vector<pair<int,int>> bestP = {{0,0}, {1,0}, {1,1}, {0,1}};
    int best = 0;
    
    // Generate many candidate boxes
    for(int tries=0; tries<5000; ++tries) {
        // Random box around mackerel cluster
        int minx = MX, maxx = 0, miny = MX, maxy = 0;
        if(mack.empty()) continue;
        int idx = rand() % N;
        minx = min(minx, mack[idx].first); maxx = max(maxx, mack[idx].first);
        miny = min(miny, mack[idx].second); maxy = max(maxy, mack[idx].second);
        
        minx = max(0, minx - 5); maxx = min(MX, maxx + 5);
        miny = max(0, miny - 5); maxy = min(MX, maxy + 5);
        if(minx > maxx) swap(minx, maxx);
        if(miny > maxy) swap(miny, maxy);
        if(minx == maxx || miny == maxy) continue;
        
        vector<pair<int,int>> box = {{minx, maxy}, {maxx, maxy}, {maxx, miny}, {minx, miny}};
        int s = score(box);
        if(s > best) { best = s; bestP = box; }
    }
    
    // Local optimization
    for(int iter=0; iter<300; ++iter) {
        vector<pair<int,int>> NP = bestP;
        int typ = rand() % 5;
        if(typ == 0) {
            for(auto& p : NP) {
                p.first = max(0, min(MX, p.first + (rand()%41-20)));
                p.second = max(0, min(MX, p.second + (rand()%41-20)));
            }
        } else if(typ == 1 && NP.size() >= 4) {
            int i = rand() % NP.size();
            pair<int,int> a = NP[i];
            int d = abs(rand() % 21 - 10); d = max(1, d);
            NP[i] = {a.first + (a.first == NP[(i+1)%NP.size()].first ? d : 0), a.second + (a.second == NP[(i+1)%NP.size()].second ? d : 0)};
        } else if(typ == 2 && NP.size() < MV - 2) {
            int i = rand() % NP.size();
            NP.insert(NP.begin()+i+1, {NP[i].first, NP[i].second + (rand()%2?5:-5)});
        } else if(typ == 3 && NP.size() > 4) {
            int i = rand() % NP.size();
            NP.erase(NP.begin()+i);
        } else {
            // Try corner cutout
            int i = rand() % NP.size();
            pair<int,int> a = NP[i], b = NP[(i+1)%NP.size()];
            if(a.first == b.first) {
                int indent = 5 + rand() % 30;
                pair<int,int> cut = {a.first + (rand()%2?1:-1)*indent, (a.second + b.second) / 2};
                cut.first = max(0, min(MX, cut.first));
                NP.insert(NP.begin()+i+1, cut);
            } else {
                int indent = 5 + rand() % 30;
                pair<int,int> cut = {(a.first + b.first) / 2, a.second + (rand()%2?1:-1)*indent};
                cut.second = max(0, min(MX, cut.second));
                NP.insert(NP.begin()+i+1, cut);
            }
        }
        
        if(NP.size() < 4 || NP.size() > MV) continue;
        long long per = 0;
        for(int i=0; i<NP.size(); ++i) per += abs(NP[i].first - NP[(i+1)%NP.size()].first) + abs(NP[i].second - NP[(i+1)%NP.size()].second);
        if(per > MP) continue;
        for(auto& p : NP) if(p.first < 0 || p.first > MX || p.second < 0 || p.second > MX) continue;
        for(int i=0; i<NP.size(); ++i) {
            pair<int,int> a = NP[i], b = NP[(i+1)%NP.size()];
            if(a.first != b.first && a.second != b.second) continue;
            if(a.first == b.first && a.second == b.second) continue;
        }
        
        int diff = score(NP);
        if(diff > best) { bestP = NP; best = diff; }
    }
    
    cout << bestP.size() << "\\n";
    for(auto& p : bestP) cout << p.first << " " << p.second << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
