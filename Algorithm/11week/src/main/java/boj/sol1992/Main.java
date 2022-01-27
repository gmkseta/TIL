package boj.sol1992;


import java.io.*;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static int N;
    static int[][] board;

    public static void main(String[] args) {
        input();
        sb.append(rec_func(0, 0, N));
        System.out.println(sb.toString());
    }


    static String rec_func(int x, int y, int k) {
        if (k == 1) {
            return board[x][y] + "";
        } else {
            String left_top = rec_func(x, y, k / 2);
            String right_top = rec_func(x, y + k / 2, k / 2);
            String left_bottom = rec_func(x + k / 2, y, k / 2);
            String right_bottom = rec_func(x + k / 2, y + k / 2, k / 2);
            if (left_top.equals(right_top) &&
                    left_top.equals(left_bottom) &&
                    left_top.equals(right_bottom) &&
                    (left_top.equals("1") || left_top.equals("0"))) {
                return left_top;
            } else {
                return "(" + left_top + right_top + left_bottom + right_bottom + ")";
            }
        }
    }


    static void input() {
        N = scan.nextInt();
        board = new int[N][N];
        for (int i = 0; i < N; i++) {
            String line = scan.next();
            for (int j = 0; j < N; j++) {
                board[i][j] = line.charAt(j) - '0';
            }
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
