package boj.sol6064;


import java.io.*;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static int T;
    static int[][] arr;

    public static void main(String[] args) {
        input();
        solution();
        System.out.println(sb.toString());
    }

    static void solution() {
        for (int i = 0; i < T; i++) {
            int m = arr[i][0];
            int n = arr[i][1];
            int x = arr[i][2];
            int y = arr[i][3];
            int cnt = x % (m + 1);
            int tempY = x;
            for (int j = 0; j < n; j++) {
                int ty = tempY % n == 0 ? n : tempY % n;
                if (ty == y) {
                    break;
                }

                tempY = ty + m;
                cnt += m;
            }
            sb.append(cnt > lcm(m, n) ? "-1" : cnt);
            sb.append("\n");
        }

    }


    static void input() {
        T = scan.nextInt();
        arr = new int[T][4];
        for (int t = 0; t < T; t++) {
            arr[t][0] = scan.nextInt();
            arr[t][1] = scan.nextInt();
            arr[t][2] = scan.nextInt();
            arr[t][3] = scan.nextInt();
        }
    }

    static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    static int lcm(int a, int b) {
        return a * b / gcd(a, b);
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
