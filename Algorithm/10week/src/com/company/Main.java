package com.company;

import java.io.*;
import java.util.ArrayList;

public class Main {
    static final BufferedReader br = new BufferedReader(new InputStreamReader(System.in)); // 입력
    static final BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out)); // 출력

    public static void main(String[] args) throws IOException {
        int n = Integer.parseInt(br.readLine());
        int[][] arr = new int[n][n];
        for(int i = 0; i < n; i++) {
            String[] str = br.readLine().split("");
            for(int j = 0; j < n; j++) {
                arr[i][j] = Integer.parseInt(str[j]);
            }
        }
        int[] answer = solution(n, arr);
        for(int i=0; i < answer.length; i++) {
            System.out.println(answer[i]);
        }

    }
    public static int[] solution(int n, int[][] map){
        int[][] direction = {{0,1},{0,-1},{1,0},{-1,0}};
        int[][] visited = new int[n][n];
        ArrayList<Integer> answer = new ArrayList<>();


        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (map[i][j] == 1 && visited[i][j] == 0){
                    ArrayList<Integer> needVisit = new ArrayList<Integer>();
                    needVisit.add(i*n+j);
                    int counter = 0;
                    while (!needVisit.isEmpty()){
                        int cur = needVisit.remove(0);
                        int x = cur/n;
                        int y = cur%n;
                        if(visited[x][y] == 1){
                            continue;
                        }else{
                            counter++;
                        }
                        visited[x][y] = 1;
                        for (int k = 0; k < 4; k++) {
                            int nextX = x + direction[k][0];
                            int nextY = y + direction[k][1];
                            if (nextX >= 0 && nextX < n && nextY >= 0 && nextY < n && map[nextX][nextY] == 1 && visited[nextX][nextY] == 0){
                                needVisit.add(nextX*n+nextY);
                            }
                        }
                    }
                    answer.add(counter);
                }
            }
        }

        answer.sort(Integer::compareTo);
        answer.add(0, answer.size());

        return answer.stream().mapToInt(i->i).toArray();
    }
    
    

}
