package codi4_2;

import java.util.HashSet;

public class Main {
    public static void main(String[] args) {
        int[] A = {4,1,3};
        solution(A);

    }

    private static int solution(int[] A) {
        HashSet<Integer> set = new HashSet<>();
        for (int i = 1; i <= A.length; i++) {
            set.add(i);
        }

        for (int i = 0; i < A.length; i++) {
            set.remove(A[i]);
        }

        if(set.isEmpty()){
            return 1;
        }else{
            return 0;
        }
    }


}
