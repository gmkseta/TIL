package boj.sol14888;

import java.io.*;
import java.util.StringTokenizer;

public class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static int N;
    static int[] nums;
    static int[] operators;
    static int[] orders;
    static int max;
    static int min;


    public static void main(String[] args) {
        input();
        rec_func(0, nums[0]);
        sb.append(max).append("\n").append(min);
        System.out.println(sb.toString());
    }

    static int calc(int operand1, int operator, int operand2) {
        switch (operator) {
            case 0:
                operand1 += operand2;
                break;
            case 1:
                operand1 -= operand2;
                break;
            case 2:
                operand1 *= operand2;
                break;
            case 3:
                operand1 /= operand2;
                break;
        }
        return operand1;
    }


    static void rec_func(int k, int value) {
        if (k == N - 1) {
//            int value = calc();
            max = Math.max(max, value);
            min = Math.min(min, value);
            return;
        } else {
            for (int i = 0; i < 4; i++) {
                if (operators[i] >= 1) {
                    operators[i]--;
                    rec_func(k + 1, calc(value, i, nums[k + 1]));
                    operators[i]++;
                }
            }
        }
    }


    static void input() {
        N = scan.nextInt();
        nums = new int[N + 1];
        operators = new int[4];
        orders = new int[N + 1];
        for (int i = 0; i < N; i++) nums[i] = scan.nextInt();
        for (int i = 0; i < 4; i++) operators[i] = scan.nextInt();
        max = Integer.MIN_VALUE;
        min = Integer.MAX_VALUE;
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
