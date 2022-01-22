package codi4_1;

import java.util.HashSet;

public class Main {
    public static void main(String[] args) {
        int[] A = {1, 3, 1, 4, 2, 3, 5, 4};
        System.out.println(solution(5, A));
    }

    private static int solution(int X, int[] A) {
        HashSet<Integer> set = new HashSet<Integer>();

        for (int i = 1; i <= X; i++) {
            set.add(i);
        }

        for (int i = 0; i < A.length; i++) {
            set.remove(A[i]);
            if(set.isEmpty()){
                return i;
            }
        }
        
        return -1;

    }
}
