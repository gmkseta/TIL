package boj.sol15312;

import java.io.*;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static int[] alpha = {3, 2, 1, 2, 3, 3, 2, 3, 3, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1};
    static String A;
    static String B;

    public static void main(String[] args) {
        input();
        System.out.println(solution());
    }


    static String solution() {
        int length = A.length();
        int[] dp = new int[2 * length];
        for (int i = 0; i < length; i++) {
            dp[2 * i] = alpha[A.charAt(i) - 'A'];
            dp[2 * i + 1] = alpha[B.charAt(i) - 'A'];
        }
        for (int i = 2 * length - 1; i > 1; i--) {
            for (int j = 0; j < i; j++) {
                dp[j] = (dp[j] + dp[j + 1]) % 10;
            }

        }


        return dp[0] + "" + dp[1];
    }


    static void input() {
        A = scan.next();
        B = scan.next();
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
