package codi3_2;

import java.util.HashSet;

public class Main {
    public static void main(String[] args) {
        int[] A = {2,3,1,5};
        System.out.println(solution(A));
    }

    private static int solution(int[] A) {
        HashSet<Integer> set = new HashSet<Integer>();
        for (int i = 1; i <= A.length+1; i++) {
            set.add(i);
        }
        for(int i : A){
            set.remove(i);
        }


        return set.iterator().next();



    }
}
