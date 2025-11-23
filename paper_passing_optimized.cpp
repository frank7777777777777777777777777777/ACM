#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
using namespace std;

/*
传纸条问题 - 空间优化版本

使用滚动数组优化空间复杂度从 O((m+n) × m × m) 降到 O(m × m)
*/

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<int>> grid(m + 1, vector<int>(n + 1));
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> grid[i][j];
        }
    }
    
    // 使用滚动数组，只保存当前步和前一步的状态
    vector<vector<int>> prev(m + 1, vector<int>(m + 1, -1));
    vector<vector<int>> curr(m + 1, vector<int>(m + 1, -1));
    
    // 初始化：两条路径都从(1,1)开始
    prev[1][1] = grid[1][1];
    
    // 状态转移
    for (int step = 1; step < m + n - 1; step++) {
        // 清空当前步的状态
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= m; j++) {
                curr[i][j] = -1;
            }
        }
        
        for (int i1 = 1; i1 <= m; i1++) {
            for (int i2 = 1; i2 <= m; i2++) {
                int j1 = step + 2 - i1;
                int j2 = step + 2 - i2;
                
                // 检查边界
                if (j1 < 1 || j1 > n || j2 < 1 || j2 > n) continue;
                
                // 计算当前位置的价值
                int value = 0;
                if (i1 == i2 && j1 == j2) {
                    value = grid[i1][j1];
                } else {
                    value = grid[i1][j1] + grid[i2][j2];
                }
                
                // 从前一步的四种状态转移而来
                int maxPrev = -1;
                
                if (i1 - 1 >= 1 && i2 - 1 >= 1 && prev[i1 - 1][i2 - 1] != -1) {
                    maxPrev = max(maxPrev, prev[i1 - 1][i2 - 1]);
                }
                
                if (i1 - 1 >= 1 && prev[i1 - 1][i2] != -1) {
                    maxPrev = max(maxPrev, prev[i1 - 1][i2]);
                }
                
                if (i2 - 1 >= 1 && prev[i1][i2 - 1] != -1) {
                    maxPrev = max(maxPrev, prev[i1][i2 - 1]);
                }
                
                if (prev[i1][i2] != -1) {
                    maxPrev = max(maxPrev, prev[i1][i2]);
                }
                
                if (maxPrev != -1) {
                    curr[i1][i2] = maxPrev + value;
                }
            }
        }
        
        // 交换prev和curr
        prev = curr;
    }
    
    cout << prev[m][m] << endl;
    
    return 0;
}