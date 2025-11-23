#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

/**
 * 矩阵取数游戏 - NOIP 2007 (简化版本)
 * 使用区间动态规划解决
 * 
 * 注意：此版本使用long long，适用于m<=60的情况
 * 对于更大的m值，需要使用高精度算法（推荐Python版本）
 */

// 对单行使用区间DP求解最大得分
long long solveSingleRow(const vector<int>& row, int m) {
    if (m == 1) {
        return (long long)row[0] * 2;
    }
    
    vector<vector<long long>> dp(m, vector<long long>(m, 0));
    
    // 预计算2的幂次
    vector<long long> powersOf2(m + 1);
    powersOf2[1] = 2;
    for (int i = 2; i <= m; i++) {
        powersOf2[i] = powersOf2[i - 1] * 2;
    }
    
    // 区间长度从1到m
    for (int length = 1; length <= m; length++) {
        int roundNum = m - length + 1;
        long long power = powersOf2[roundNum];
        
        for (int i = 0; i <= m - length; i++) {
            int j = i + length - 1;
            
            if (length == 1) {
                dp[i][j] = (long long)row[i] * power;
            } else {
                long long takeLeft = dp[i + 1][j] + (long long)row[i] * power;
                long long takeRight = dp[i][j - 1] + (long long)row[j] * power;
                dp[i][j] = max(takeLeft, takeRight);
            }
        }
    }
    
    return dp[0][m - 1];
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> matrix(n, vector<int>(m));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> matrix[i][j];
        }
    }
    
    long long totalScore = 0;
    for (int i = 0; i < n; i++) {
        totalScore += solveSingleRow(matrix[i], m);
    }
    
    cout << totalScore << endl;
    
    return 0;
}