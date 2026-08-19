# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

// === MACROS AND CONSTANTS ===
const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;

// === DATA STRUCTURES ===
struct Fish {
    int x, y, type;
};
std::vector<Fish> fish_data;

// === SCORING ===
int count_fish_in_rect(int x1, int y1, int x2, int y2) {
    int m_count = 0, s_count = 0;
    for (const auto& f : fish_data) {
        if (f.x >= x1 && f.x <= x2 && f.y >= y1 && f.y <= y2) {
            if (f.type == 1) m_count++;
            else s_count++;
        }
    }
    return m_count - s_count;
}

// === GREASY RECTANGLE SEARCH ===
int best_score = -1e9;
int best_x1, best_y1, best_x2, best_y2;

void greedy_rectangle_search(int max_iterations = 10000) {
    // Sample random rectangles
    std::srand(42);
    
    // Get bounding box of all fish
    int min_x = MAX_COORD_VAL, max_x = 0, min_y = MAX_COORD_VAL, max_y = 0;
    for (const auto& f : fish_data) {
        min_x = std::min(min_x, f.x);
        max_x = std::max(max_x, f.x);
        min_y = std::min(min_y, f.y);
        max_y = std::max(max_y, f.y);
    }
    
    // Add some margin
    min_x = std::max(0, min_x - 10);
    max_x = std::min(MAX_COORD_VAL, max_x + 10);
    min_y = std::max(0, min_y - 10);
    max_y = std::min(MAX_COORD_VAL, max_y + 10);
    
    // Try rectangles at fish locations
    for (const auto& f : fish_data) {
        for (int dx = 0; dx <= 5000 && count_fish_in_rect(f.x, f.y, f.x + dx, f.y) >= 0; dx += std::max(1, dx/2)) {
            for (int dy = 0; dy <= 5000 && count_fish_in_rect(f.x, f.y, f.x + dx, f.y + dy) >= 0; dy += std::max(1, dy/2)) {
                int score = count_fish_in_rect(f.x, f.y, f.x + dx, f.y + dy);
                if (score > best_score) {
                    best_score = score;
                    best_x1 = f.x;
                    best_y1 = f.y;
                    best_x2 = f.x + dx;
                    best_y2 = f.y + dy;
                }
                if (best_score > 1000) break; // Early exit if we found good score
            }
            if (best_score > 1000) break;
        }
        if (best_score > 1000) break;
    }
    
    // Also try expanding from best found
    for (int dx = 0; dx <= 10000 && best_x2 + dx <= MAX_COORD_VAL; dx += std::max(1, dx/4)) {
        for (int dy = 0; dy <= 10000 && best_y2 + dy <= MAX_COORD_VAL; dy += std::max(1, dy/4)) {
            int score = count_fish_in_rect(best_x1, best_y1, best_x2 + dx, best_y2 + dy);
            if (score > best_score) {
                best_score = score;
                best_x2 = best_x2 + dx;
                best_y2 = best_y2 + dy;
            }
        }
    }
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    std::cin >> N;
    
    fish_data.resize(2 * N);
    
    // Read mackerels
    for (int i = 0; i < N; ++i) {
        std::cin >> fish_data[i].x >> fish_data[i].y;
        fish_data[i].type = 1;
    }
    
    // Read sardines
    for (int i = 0; i < N; ++i) {
        std::cin >> fish_data[N + i].x >> fish_data[N + i].y;
        fish_data[N + i].type = -1;
    }
    
    // Ensure we have a valid rectangle
    if (best_score <= -1e8) {
        best_score = 0;
        best_x1 = 0; best_y1 = 0; best_x2 = 1; best_y2 = 1;
    }
    
    // Output rectangle as 4 vertices (clockwise)
    std::cout << 4 << "\\n";
    std::cout << best_x1 << " " << best_y1 << "\\n";
    std::cout << best_x2 << " " << best_y1 << "\\n";
    std::cout << best_x2 << " " << best_y2 << "\\n";
    std::cout << best_x1 << " " << best_y2 << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
