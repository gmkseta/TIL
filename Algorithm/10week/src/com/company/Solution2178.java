package com.company;

import java.util.ArrayList;

public class Solution2178 {
    public static int solve(int n, int m, int[][] board){
        int[][] direction = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        ArrayList<Integer> need_visited = new ArrayList<>();
        int[][] dp = new int[n][m]

        need_visited.add(0);
        while(!need_visited.isEmpty()){
            int idx = need_visited.remove(0);
            int y = idx / m;
            int x = idx % m;
            for (int i = 0; i < 4; i++) {
                int dx = direction[i][0], dy = direction[i][1];
                int nx = x + dx, ny = y + dx;
                if(nx < 0 || ny < 0 || nx >= m || ny >= n){
                    continue;
                }
                if(board[nx][ny] == 0){
                    continue;
                }





            }





        }




    }
}
