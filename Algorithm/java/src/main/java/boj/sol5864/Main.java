package boj.sol5864;

import java.util.*;
import java.io.*;
import java.awt.Point;

import static java.lang.Math.*;

public class Main {
    static int n;
    static int A;
    static int B;
    static int[] X = new int[n];


    public static void main(String[] args) throws Exception {
        Scanner in = new Scanner(new File("/Users/seongjunkim/Downloads/wifi/3.in"));
        n = in.nextInt();
        A = in.nextInt();
        B = in.nextInt();
        X = new int[n];
        f_s = new boolean[n];
        f = new double[n];
        for (int i = 0; i < n; i++) X[i] = in.nextInt();
        Arrays.sort(X);
        double ans = f(0);
        if (abs(ans - (int) (ans + 0.5)) < 1e-9)
            System.out.println((int) (ans + 0.5));
        else System.out.println(ans);
        System.out.flush();
    }


    static boolean[] f_s;
    static double[] f;

    static double f(int i) {
        if (i >= n) return 0;
        if (f_s[i]) return f[i];
        f_s[i] = true;
        double ans = 1000.0 * 1000 * 1000 * 1000;
        for (int j = i; j < n; j++) { // end of range
            ans = min(ans, A + B * (X[j] - X[i]) / 2.0 + f(j + 1));
        }
        return f[i] = ans;
    }
}
