# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <bits/stdc++.h>
using namespace std;

struct Pt { int x,y; };

vector<Pt> fish;

int main() {
    int N;
    cin >> N;
    fish.resize(2*N);
    for(int i=0; i<N; ++i) {
        cin >> fish[i].x >> fish[i].y;
    }
    for(int i=0; i<N; ++i) {
        cin >> fish[N+i].x >> fish[N+i].y;
    }
    
    // Just output first mackerel's location as a small square
    Pt p[4];
    p[0] = {fish[0].x - 250, fish[0].y - 250};
    p[1] = {fish[0].x + 250, fish[0].y - 250};
    p[2] = {fish[0].x + 250, fish[0].y + 250};
    p[3] = {fish[0].x - 250, fish[0].y + 250};
    
    // Clamp to bounds
    for(int i=0; i<4; ++i) {
        p[i].x = max(0, min(100000, p[i].x));
        p[i].y = max(0, min(100000, p[i].y));
    }
    
    cout << 4 << "\\n";
    for(int i=0; i<4; ++i) cout << p[i].x << " " << p[i].y << "\\n";
    return 0;
}
'''
# EVOLVE-BLOCK-END
