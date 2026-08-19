# EVOLVE-BLOCK-START
CPP_CODE = '''
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>

const int MAX_COORD = 100000;
const int MAX_X = 10005;
const int MAX_Y = 10005;
const int MAX_ITER = 10;
const int REFINEMENT = 4;

struct Fish { int x,y,t; };
struct Cell { int m,s,sc; };
Cell g[MAX_Y][MAX_X];

void build(const std::vector<Fish>& f) {
    for(auto& x:f) {
        int r=x.y/MAX_X,c=x.x/MAX_X;
        if(x.t==1) g[r][c].m++; else g[r][c].s++;
    }
    for(int i=0;i<MAX_Y;i++)
        for(int j=0;j<MAX_X;j++)
            g[i][j].sc=g[i][j].m-g[i][j].s;
}

int count_rect(int x1,int y1,int x2,int y2,const std::vector<Fish>& f,int type) {
    int cnt=0;
    for(const auto& fish:f) {
        if(fish.t==type && fish.x>=x1 && fish.x<=x2 && fish.y>=y1 && fish.y<=y2) cnt++;
    }
    return cnt;
}

void expand_all_directions(int sr,int sc,std::vector<std::pair<int,int>>& out,
                           const Cell grid[MAX_Y][MAX_X],int max_len=12) {
    out.push_back(std::make_pair(sc * MAX_X, sr * MAX_X));
    int dr[] = {-1, 1, 0, 0};
    int dc[] = {0, 0, -1, 1};
    
    for(int d = 0; d < 4; d++) {
        int r = sr, c = sc;
        for(int i = 0; i < max_len; i++) {
            int nr = r + dr[d];
            int nc = c + dc[d];
            
            if(nr < 0 || nr >= MAX_Y || nc < 0 || nc >= MAX_X) break;
            int diff = grid[nr][nc].sc;
            if(diff < 0 || grid[nr][nc].s > grid[nr][nc].m + 2) break;
            
            out.push_back(std::make_pair(nc * MAX_X, nr * MAX_X));
            r = nr; c = nc;
        }
    }
}

void hill_climb_rect(int& x1,int& y1,int& x2,int& y2,const std::vector<Fish>& f) {
    int bm = count_rect(x1,y1,x2,y2,f,1);
    int bs = count_rect(x1,y1,x2,y2,f,-1);
    int best_diff = bm - bs;
    int best_dx = 0, best_dy = 0;
    
    for(int round = 0; round < 2; round++) {
        for(int dy = -REFINEMENT * (round + 1); dy <= REFINEMENT * (round + 1); dy++) {
            for(int dx = -REFINEMENT * (round + 1); dx <= REFINEMENT * (round + 1); dx++) {
                int nx = x1 + dx, ny = y1 + dy;
                int nx2 = x2 + dx, ny2 = y2 + dy;
                
                if(nx < 0 || ny < 0 || nx2 > MAX_COORD || ny2 > MAX_COORD) continue;
                if(nx > nx2 || ny > ny2) continue;
                
                int cm = count_rect(nx,ny,nx2,ny2,f,1);
                int cs = count_rect(nx,ny,nx2,ny2,f,-1);
                int diff = cm - cs;
                
                if(diff > best_diff) {
                    best_diff = diff;
                    best_dx = dx;
                    best_dy = dy;
                    bm = cm;
                    bs = cs;
                }
            }
        }
    }
    
    x1 += best_dx;
    y1 += best_dy;
    x2 += best_dx;
    y2 += best_dy;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    std::cin >> N;
    
    std::vector<Fish> mackerels(N), sardines(N), all_fish(2*N);
    
    for(int i = 0; i < N; i++) {
        std::cin >> mackerels[i].x >> mackerels[i].y;
        mackerels[i].t = 1;
        all_fish[i] = mackerels[i];
    }
    
    for(int i = 0; i < N; i++) {
        std::cin >> sardines[i].x >> sardines[i].y;
        sardines[i].t = -1;
        all_fish[N + i] = sardines[i];
    }
    
    build(all_fish);
    
    int best_score = 0;
    int best_x1 = 0, best_y1 = 0, best_x2 = 0, best_y2 = 0;
    
    for(int restart = 0; restart < MAX_ITER; restart++) {
        std::vector<std::pair<int,int>> positive_cells;
        for(int i = 0; i < MAX_Y; i++) {
            for(int j = 0; j < MAX_X; j++) {
                if(g[i][j].sc > 0) {
                    positive_cells.push_back(std::make_pair(j * MAX_X + i, g[i][j].sc));
                }
            }
        }
        
        std::sort(positive_cells.begin(), positive_cells.end(),
                 [](const std::pair<int,int>& a, const std::pair<int,int>& b) {
                     return a.second > b.second;
                 });
        
        std::mt19937 gen(std::chrono::steady_clock::now().time_since_epoch().count());
        std::shuffle(positive_cells.begin(), positive_cells.end(), gen);
        
        for(const auto& cell : positive_cells) {
            int sr = cell.first / MAX_X;
            int sc = cell.first % MAX_X;
            
            std::vector<std::pair<int,int>> corridors;
            expand_all_directions(sr, sc, corridors, g, 12);
            
            if(corridors.empty()) continue;
            
            int x1 = MAX_COORD, x2 = -1, y1 = MAX_COORD, y2 = -1;
            for(const auto& pt : corridors) {
                x1 = std::min(x1, pt.first);
                x2 = std::max(x2, pt.first);
                y1 = std::min(y1, pt.second);
                y2 = std::max(y2, pt.second);
            }
            
            if(x1 > MAX_COORD || y1 > MAX_COORD || x2 < 0 || y2 < 0) continue;
            x1 = std::max(0, x1);
            y1 = std::max(0, y1);
            x2 = std::min(MAX_COORD, x2);
            y2 = std::min(MAX_COORD, y2);
            
            if(x1 > x2 || y1 > y2) continue;
            
            int m_cnt = count_rect(x1,y1,x2,y2,all_fish,1);
            int s_cnt = count_rect(x1,y1,x2,y2,all_fish,-1);
            int score = m_cnt - s_cnt + 1;
            
            if(score > best_score) {
                best_score = score;
                best_x1 = x1;
                best_y1 = y1;
                best_x2 = x2;
                best_y2 = y2;
            }
            
            hill_climb_rect(best_x1, best_y1, best_x2, best_y2, all_fish);
            
            m_cnt = count_rect(best_x1,best_y1,best_x2,best_y2,all_fish,1);
            s_cnt = count_rect(best_x1,best_y1,best_x2,best_y2,all_fish,-1);
            score = m_cnt - s_cnt + 1;
            
            if(score > best_score) {
                best_score = score;
                best_x1 = best_x1;
                best_y1 = best_y1;
                best_x2 = best_x2;
                best_y2 = best_y2;
            }
            
            if(best_score <= 0) break;
        }
    }
    
    std::cout << 4 << "\\n";
    std::cout << best_x1 << " " << best_y1 << "\\n";
    std::cout << best_x2 << " " << best_y1 << "\\n";
    std::cout << best_x2 << " " << best_y2 << "\\n";
    std::cout << best_x1 << " " << best_y2 << "\\n";
    
    return 0;
}
'''
# EVOLVE-BLOCK-END
