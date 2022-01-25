package boj.sol13301;

import java.io.*;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static long K;

    public static void main(String[] args) {
        input();
        System.out.println(solution());
    }


    static long solution() {
        /**
         * 1 * 4 = 4
         * 4 + 4 - 2 = 6
         * 6 - 2 + 2 * 3 = 10
         * 10 - 3 + 3 * 3 = 16
         * 16 - 5 + 5 * 3 = 26
         * 이전꺼
         */
        long dp[] = {4, 6};
        long fibo[] = {1, 1};

        for (int i = 2; i < K; i++) {
            long length = fibo[0] + fibo[1];
            fibo[0] = fibo[1];
            fibo[1] = length;

            long round = dp[1] + length * 2;
            dp[0] = dp[1];
            dp[1] = round;
        }

        if (K == 1) {
            return dp[0];
        } else {
            return dp[1];

        }
    }


    static void input() {
        K = scan.nextLong();
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
