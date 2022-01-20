package codi3_3;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] A = {3};
        System.out.println(solution(A));
    }
    public static int solution(int[] A){
        int left = 0;
        int right = Arrays.stream(A).sum();
        int min = Integer.MAX_VALUE;
        for(int i = 0; i < A.length; i++){
            left+=A[i];
            right-=A[i];
            min = Math.min(
                    min, Math.abs(left - right)
            );
        }

        return min;
    }
}

