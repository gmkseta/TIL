package boj.sol9663;

import java.io.*;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static int N;
    static int[] col;
    static int ans = 0;

    public static void main(String[] args) {
        input();
        rec_func(0);
        sb.append(ans);
        System.out.println(sb.toString());
    }

    static boolean validity_check(int row, int i) {
        for (int j = 0; j < row; j++) {
            if (attackable(row, i, j, col[j])) {
                return false;
            }
        }
        return true;
    }

    private static boolean attackable(int r1, int c1, int r2, int c2) {
        if (c1 == c2) {
            return true;
        } else if (r1 - c1 == r2 - c2) {
            return true;
        } else if (r1 + c1 == r2 + c2) {
            return true;
        }
        return false;
    }

    private static void rec_func(int row) {
        if (row == N) {
            ans++;
        } else {
            for (int i = 0; i < N; i++) {
                if (validity_check(row, i)) {
                    col[row] = i;
                    rec_func(row + 1);
                    col[row] = 0;
                }
            }
        }
    }


    static int solution() {
        return 1;
    }


    static void input() {
        N = scan.nextInt();
        col = new int[N + 1];
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
