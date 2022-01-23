package boj.sol1446;

import java.io.*;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static int N;
    static int D;
    static int[][] road;


    public static void main(String[] args) {
        input();
        System.out.println(solution(N, D, road));
    }


    static int solution(int N, int D, int[][] road) {
        int[][] sortedRoad = Arrays.stream(road).sorted((a, b) -> a[0] - b[0]).toArray(int[][]::new);
        int[] dp = new int[10001];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;
        int idx = 0, move = 0;
        while (move < D) {
            if (idx < sortedRoad.length && move == sortedRoad[idx][0]) {
                dp[sortedRoad[idx][1]] = Math.min(
                        dp[move] + sortedRoad[idx][2],
                        dp[sortedRoad[idx][1]]);
                idx++;
            } else {
                dp[move + 1] = Math.min(dp[move + 1], dp[move] + 1);
                move++;
            }
        }

        return dp[D];
    }


    static void input() {
        N = scan.nextInt();
        D = scan.nextInt();
        road = new int[N][3];
        for (int i = 0; i < N; i++) {
            road[i][0] = scan.nextInt();
            road[i][1] = scan.nextInt();
            road[i][2] = scan.nextInt();
        }
    }

    static class FastReader {
        BufferedReader br;
        StringTokenizer st;

        public FastReader() {
            br = new BufferedReader(new InputStreamReader(System.in));
        }

        public FastReader(String s) throws FileNotFoundException {
            br = new BufferedReader(new FileReader(new File(s)));
        }

        String next() {
            while (st == null || !st.hasMoreElements()) {
                try {
                    st = new StringTokenizer(br.readLine());
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return st.nextToken();
        }

        int nextInt() {
            return Integer.parseInt(next());
        }

        long nextLong() {
            return Long.parseLong(next());
        }

        double nextDouble() {
            return Double.parseDouble(next());
        }

        String nextLine() {
            String str = "";
            try {
                str = br.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return str;
        }
    }

}
