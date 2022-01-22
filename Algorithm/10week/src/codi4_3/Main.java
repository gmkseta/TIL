package codi4_3;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] A={3,4,4,6,1,4,4};
        System.out.println(Arrays.toString(solution(5,A)));
    }

    private static int[] solution(int N, int[] A) {
        int[] counters = new int[N];
        int max = 0;
        int count = 0;
        for (int i = 0; i < A.length; i++) {
            if(A[i]==N+1){
                counters = new int[N];
                count=max;
            }else{
                counters[A[i]-1]+=1;
                max = Math.max(counters[A[i]-1], max);
            }

        }
        for (int i = 0; i < N; i++) {
            counters[i]+=count;
        }
        return counters;
    }

}
