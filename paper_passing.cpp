#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>
using namespace std;

int main() {
    int m, n;
    cin >> m >> n;
    
    vector<vector<int>> grid(m + 1, vector<int>(n + 1));
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> grid[i][j];
        }
    }
    
    // dp[step][i1][i2] 表示走了step步，第一条路径在第i1行，第二条路径在第i2行时的最大值
    // 由于 i1 + j1 = i2 + j2 = step + 2，所以 j1 = step + 2 - i1, j2 = step + 2 - i2
    vector<vector<vector<int>>> dp(m + n, vector<vector<int>>(m + 1, vector<int>(m + 1, -1)));
    
    // 初始化：两条路径都从(1,1)开始
    dp[0][1][1] = grid[1][1];
    
    // 状态转移
    for (int step = 1; step < m + n - 1; step++) {
        for (int i1 = 1; i1 <= m; i1++) {
            for (int i2 = 1; i2 <= m; i2++) {
                int j1 = step + 2 - i1;
                int j2 = step + 2 - i2;
                
                // 检查边界
                if (j1 < 1 || j1 > n || j2 < 1 || j2 > n) continue;
                
                // 计算当前位置的价值
                int value = 0;
                if (i1 == i2 && j1 == j2) {
                    // 两条路径在同一位置，只能取一次
                    value = grid[i1][j1];
                } else {
                    // 两条路径在不同位置
                    value = grid[i1][j1] + grid[i2][j2];
                }
                
                // 从前一步的四种状态转移而来
                int maxPrev = -1;
                
                // 第一条路径从上方来，第二条路径从上方来
                if (i1 - 1 >= 1 && i2 - 1 >= 1 && dp[step - 1][i1 - 1][i2 - 1] != -1) {
                    maxPrev = max(maxPrev, dp[step - 1][i1 - 1][i2 - 1]);
                }
                
                // 第一条路径从上方来，第二条路径从左方来
                if (i1 - 1 >= 1 && dp[step - 1][i1 - 1][i2] != -1) {
                    maxPrev = max(maxPrev, dp[step - 1][i1 - 1][i2]);
                }
                
                // 第一条路径从左方来，第二条路径从上方来
                if (i2 - 1 >= 1 && dp[step - 1][i1][i2 - 1] != -1) {
                    maxPrev = max(maxPrev, dp[step - 1][i1][i2 - 1]);
                }
                
                // 第一条路径从左方来，第二条路径从左方来
                if (dp[step - 1][i1][i2] != -1) {
                    maxPrev = max(maxPrev, dp[step - 1][i1][i2]);
                }
                
                if (maxPrev != -1) {
                    dp[step][i1][i2] = maxPrev + value;
                }
            }
        }
    }
    
    cout << dp[m + n - 2][m][m] << endl;
    
    return 0;
}