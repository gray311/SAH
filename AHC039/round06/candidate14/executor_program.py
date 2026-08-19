# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <numeric>

const int MAX_COORD_VAL = 100000;
const int MAX_VERTICES = 1000;
const int MAX_PERIMETER = 400000;
const int GRID_SIZE = 100; // Finer grid

struct Point {
    int x, y;
};

struct Fish {
    Point p;
    int type;
};
std::vector<Fish> all_fish;

struct Cell {
    int net_score;
};
std::vector<Cell> grid_cells;

std::vector<Point> best_poly = {{0,0}, {1,0}, {1,1}, {0,1}};
int best_score = -1e9;

int count_inside(const std::vector<Point>& poly) {
    int m = 0, s = 0;
    int n = poly.size();
    if (n < 3) return 0;
    for (const auto& f : all_fish) {
        bool inside = false;
        for (int i = 0; i < n; ++i) {
            Point a = poly[i], b = poly[(i+1)%n];
            long long cp = (long long)(b.x - a.x) * (f.p.y - a.y) - (long long)(b.y - a.y) * (f.p.x - a.x);
            if (cp == 0) {
                if (std::min(a.x, b.x) <= f.p.x && f.p.x <= std::max(a.x, b.x) &&
                    std::min(a.y, b.y) <= f.p.y && f.p.y <= std::max(a.y, b.y)) {
                    inside = true;
                    break;
                }
            } else if ((a.y <= f.p.y && b.y > f.p.y && cp > 0) ||
                       (a.y > f.p.y && b.y <= f.p.y && cp < 0)) {
                inside = true;
                break;
            }
        }
        if (inside) {
            if (f.type == 1) m++;
            else s++;
        }
    }
    return m - s;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    int N;
    std::cin >> N;
    all_fish.resize(2 * N);
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[i].p.x >> all_fish[i].p.y;
        all_fish[i].type = 1;
    }
    for (int i = 0; i < N; ++i) {
        std::cin >> all_fish[N + i].p.x >> all_fish[N + i].p.y;
        all_fish[N + i].type = -1;
    }
    
    // Build density grid
    grid_cells.resize(GRID_SIZE * GRID_SIZE);
    int cell_w = MAX_COORD_VAL / GRID_SIZE;
    int cell_h = MAX_COORD_VAL / GRID_SIZE;
    for (const auto& f : all_fish) {
        int cx = f.p.x / cell_w;
        int cy = f.p.y / cell_h;
        cx = std::min(cx, GRID_SIZE - 1);
        cy = std::min(cy, GRID_SIZE - 1);
        grid_cells[cy * GRID_SIZE + cx].net_score += f.type;
    }
    
    // Find profitable cells
    std::vector<int> profitable_cells;
    for (int i = 0; i < GRID_SIZE * GRID_SIZE; ++i) {
        if (grid_cells[i].net_score > 0) {
            profitable_cells.push_back(i);
        }
    }
    
    if (profitable_cells.empty()) {
        std::cout << best_poly.size() << "\\n";
        for (const auto& p : best_poly) {
            std::cout << p.x << " " << p.y << "\\n";
        }
        return 0;
    }
    
    // Find connected components
    std::vector<bool> visited(GRID_SIZE * GRID_SIZE, false);
    std::vector<std::vector<int>> components;
    for (int i : profitable_cells) {
        if (!visited[i]) {
            std::vector<int> comp;
            std::queue<int> q;
            q.push(i);
            visited[i] = true;
            while (!q.empty()) {
                int curr = q.front();
                q.pop();
                comp.push_back(curr);
                int cx = curr % GRID_SIZE, cy = curr / GRID_SIZE;
                int dx[] = {0, 0, 1, -1};
                int dy[] = {1, -1, 0, 0};
                for (int d = 0; d < 4; ++d) {
                    int nx = cx + dx[d], ny = cy + dy[d];
                    if (nx >= 0 && nx < GRID_SIZE && ny >= 0 && ny < GRID_SIZE &&
                        !visited[ny * GRID_SIZE + nx] && grid_cells[ny * GRID_SIZE + nx].net_score > 0) {
                        visited[ny * GRID_SIZE + nx] = true;
                        q.push(ny * GRID_SIZE + nx);
                    }
                }
            }
            if (!comp.empty()) components.push_back(comp);
        }
    }
    
    // Try each component as a bounding box
    for (const auto& comp : components) {
        int min_x = MAX_COORD_VAL, max_x = 0, min_y = MAX_COORD_VAL, max_y = 0;
        for (int idx : comp) {
            int cx = idx % GRID_SIZE, cy = idx / GRID_SIZE;
            min_x = std::min(min_x, cx * cell_w);
            max_x = std::max(max_x, (cx + 1) * cell_w - 1);
            min_y = std::min(min_y, cy * cell_h);
            max_y = std::max(max_y, (cy + 1) * cell_h - 1);
        }
        if (min_x <= max_x && min_y <= max_y) {
            std::vector<Point> poly = {{min_x, min_y}, {max_x, min_y}, {max_x, max_y}, {min_x, max_y}};
            if (poly.size() >= 4) {
                long long perim = 0;
                for (size_t i = 0; i < poly.size(); ++i) {
                    perim += std::abs(poly[i].x - poly[(i+1)%poly.size()].x) + std::abs(poly[i].y - poly[(i+1)%poly.size()].y);
                }
                if (perim <= MAX_PERIMETER) {
                    int score = count_inside(poly);
                    if (score > best_score) {
                        best_score = score;
                        best_poly = poly;
                    }
                }
            }
        }
    }
    
    // Also try individual cells
    for (int idx : profitable_cells) {
        int cx = idx % GRID_SIZE, cy = idx / GRID_SIZE;
        int x1 = cx * cell_w, y1 = cy * cell_h;
        int x2 = (cx + 1) * cell_w - 1, y2 = (cy + 1) * cell_h - 1;
        if (x1 <= x2 && y1 <= y2) {
            std::vector<Point> poly = {{x1, y1}, {x2, y1}, {x2, y2}, {x1, y2}};
            if (poly.size() >= 4) {
                long long perim = 0;
                for (size_t i = 0; i < poly.size(); ++i) {
                    perim += std::abs(poly[i].x - poly[(i+1)%poly.size()].x) + std::abs(poly[i].y - poly[(i+1)%poly.size()].y);
                }
                if (perim <= MAX_PERIMETER) {
                    int score = count_inside(poly);
                    if (score > best_score) {
                        best_score = score;
                        best_poly = poly;
                    }
                }
            }
        }
    }
    
    std::cout << best_poly.size() << "\\n";
    for (const auto& p : best_poly) {
        std::cout << p.x << " " << p.y << "\\n";
    }
    return 0;
}
'''
# EVOLVE-BLOCK-END
