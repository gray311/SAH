# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>

int main() {
    int n;
    std::cin >> n;
    
    int mx[100001] = {0};
    int my[100001] = {0};
    int sx[100001] = {0};
    int sy[100001] = {0};
    
    for(int i = 0; i < n; i++) {
        int x, y;
        std::cin >> x >> y;
        mx[x]++; my[y]++;
    }
    for(int i = 0; i < n; i++) {
        int x, y;
        std::cin >> x >> y;
        sx[x]++; sy[y]++;
    }
    
    int best_x = 50000, best_y = 50000;
    int best_m = 0, best_s = 0;
    
    for(int x = 0; x <= 100000; x += 10000) {
        for(int y = 0; y <= 100000; y += 10000) {
            int m = 0, s = 0;
            for(int xi = std::max(0, x - 5000); xi <= std::min(100000, x + 5000); xi += 10000) {
                for(int yi = std::max(0, y - 5000); yi <= std::min(100000, y + 5000); yi += 10000) {
                    m += mx[xi];
                    s += sy[yi];
                }
            }
            if(m - s > best_m - best_s) {
                best_m = m; best_s = s;
                best_x = x; best_y = y;
            }
        }
    }
    
    std::cout << 4 << std::endl;
    std::cout << best_x << " " << best_y << std::endl;
    std::cout << 100000 << " " << best_y << std::endl;
    std::cout << 100000 << " " << 100000 << std::endl;
    std::cout << best_x << " " << 100000 << std::endl;
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
