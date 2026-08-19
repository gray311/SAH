# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

const int MAXC = 100000;
const int GC = 100;

struct Pt { int x,y; };
struct Fish { Pt p; int t; };
vector<Fish> F;

int main(){
    ios::sync_with_stdio(0); cin.tie(0);
    int N; cin>>N;
    F.resize(2*N);
    for(int i=0;i<N;++i) { cin>>F[i].p.x>>F[i].p.y; F[i].t=1; }
    for(int i=0;i<N;++i) { cin>>F[N+i].p.x>>F[N+i].p.y; F[N+i].t=-1; }
    
    // Output a simple valid polygon
    cout << 4 << "\\n";
    cout << "0 0\\n";
    cout << "100000 0\\n";
    cout << "100000 100000\\n";
    cout << "0 100000\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
