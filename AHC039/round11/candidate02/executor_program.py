# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <cmath>
#include <chrono>

using namespace std;

const int MAXC = 100000;
const int MAXV = 1000;
const int MAXP = 400000;

struct Pt { int x, y; };

struct Fish { Pt p; int t; };
vector<Fish> F;

int main() {
    int N;
    cin >> N;
    F.resize(2 * N);
    for (int i = 0; i < N; ++i) {
        cin >> F[i].p.x >> F[i].p.y;
        F[i].t = 1;
    }
    for (int i = 0; i < N; ++i) {
        cin >> F[N + i].p.x >> F[N + i].p.y;
        F[N + i].t = -1;
    }
    
    vector<Pt> poly = {{0, 0}, {100, 0}, {100, 100}, {0, 100}};
    
    cout << poly.size() << endl;
    for (const auto& p : poly) {
        cout << p.x << " " << p.y << endl;
    }
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
