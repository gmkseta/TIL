package codi3;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        int[] inp = {9, 3, 9, 3, 9, 7, 9};
        System.out.println(solution(inp));
    }

    public static int solution(int[] A){
        int[] arr = Arrays.stream(A).sorted().toArray();
        for(int i = 0; i < A.length; i+=2){
            if(i+1 == A.length || arr[i] != arr[i+1]){
                return arr[i];
            }
        }
        return arr[0];
    }
}
