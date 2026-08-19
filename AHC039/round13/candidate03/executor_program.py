# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <cmath>

using namespace std;

const int MAX_COORD = 100000;
const int GRID_SIZE = 500;

struct Fish {
    int x, y, type;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<Fish> all_fish(2 * N);
    for (int i = 0; i < N; i++) {
        cin >> all_fish[i].x >> all_fish[i].y;
        all_fish[i].type = 1;
    }
    for (int i = 0; i < N; i++) {
        cin >> all_fish[N + i].x >> all_fish[N + i].y;
        all_fish[N + i].type = -1;
    }

    vector<vector<int>> grid(GRID_SIZE, vector<int>(GRID_SIZE, 0));
    for (const auto& f : all_fish) {
        int r = min(GRID_SIZE - 1, max(0, f.y / (MAX_COORD / GRID_SIZE)));
        int c = min(GRID_SIZE - 1, max(0, f.x / (MAX_COORD / GRID_SIZE)));
        grid[r][c] += f.type;
    }

    vector<vector<bool>> visited(GRID_SIZE, vector<bool>(GRID_SIZE, false));
    struct Component {
        int min_x, max_x, min_y, max_y;
    };
    vector<Component> components;

    for (int r = 0; r < GRID_SIZE; r++) {
        for (int c = 0; c < GRID_SIZE; c++) {
            if (grid[r][c] > 0 && !visited[r][c]) {
                Component comp;
                comp.min_x = comp.max_x = c;
                comp.min_y = comp.max_y = r;
                
                queue<pair<int,int>> q;
                q.push({r, c});
                visited[r][c] = true;
                
                int dr[] = {0, 0, 1, -1};
                int dc[] = {1, -1, 0, 0};
                
                while (!q.empty()) {
                    auto [cr, cc] = q.front();
                    q.pop();
                    comp.min_x = min(comp.min_x, cc);
                    comp.max_x = max(comp.max_x, cc);
                    comp.min_y = min(comp.min_y, cr);
                    comp.max_y = max(comp.max_y, cr);
                    
                    for (int i = 0; i < 4; i++) {
                        int nr = cr + dr[i];
                        int nc = cc + dc[i];
                        if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE &&
                            grid[nr][nc] > 0 && !visited[nr][nc]) {
                            visited[nr][nc] = true;
                            q.push({nr, nc});
                        }
                    }
                }
                components.push_back(comp);
            }
        }
    }

    vector<vector<int>> prefix_sum(GRID_SIZE + 1, vector<int>(GRID_SIZE + 1, 0));
    for (int r = 0; r < GRID_SIZE; r++) {
        for (int c = 0; c < GRID_SIZE; c++) {
            prefix_sum[r+1][c+1] = prefix_sum[r][c+1] + prefix_sum[r+1][c] - prefix_sum[r][c] + grid[r][c];
        }
    }

    auto count_in_rect = [&](int x1, int y1, int x2, int y2) -> int {
        if (x1 > x2 || y1 > y2) return 0;
        int r1 = min(GRID_SIZE - 1, max(0, y1 / (MAX_COORD / GRID_SIZE)));
        int r2 = min(GRID_SIZE - 1, max(0, y2 / (MAX_COORD / GRID_SIZE)));
        int c1 = min(GRID_SIZE - 1, max(0, x1 / (MAX_COORD / GRID_SIZE)));
        int c2 = min(GRID_SIZE - 1, max(0, x2 / (MAX_COORD / GRID_SIZE)));
        if (r1 > r2 || c1 > c2) return 0;
        return prefix_sum[r2+1][c2+1] - prefix_sum[r1][c2+1] - prefix_sum[r2+1][c1] + prefix_sum[r1][c1];
    };

    int best_score = -1e9;
    vector<pair<int,int>> best_rect;

    for (const auto& comp : components) {
        int x1 = comp.min_x * (MAX_COORD / GRID_SIZE);
        int y1 = comp.min_y * (MAX_COORD / GRID_SIZE);
        int x2 = (comp.max_x + 1) * (MAX_COORD / GRID_SIZE) - 1;
        int y2 = (comp.max_y + 1) * (MAX_COORD / GRID_SIZE) - 1;
        
        x1 = max(0, min(MAX_COORD, x1));
        y1 = max(0, min(MAX_COORD, y1));
        x2 = max(x1, min(MAX_COORD, x2));
        y2 = max(y1, min(MAX_COORD, y2));
        
        if (x1 == x2 || y1 == y2) continue;

        int score = count_in_rect(x1, y1, x2, y2);
        if (score > best_score) {
            best_score = score;
            best_rect = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
        }
    }

    if (best_rect.empty()) {
        best_rect = {{0, 0}, {100, 0}, {100, 100}, {0, 100}};
    }

    cout << 4 << "\\n";
    cout << best_rect[0].first << " " << best_rect[0].second << "\\n";
    cout << best_rect[1].first << " " << best_rect[1].second << "\\n";
    cout << best_rect[2].first << " " << best_rect[2].second << "\\n";
    cout << best_rect[3].first << " " << best_rect[3].second << "\\n";

    return 0;
}
'''
# EVOLVE-BLOCK-END
