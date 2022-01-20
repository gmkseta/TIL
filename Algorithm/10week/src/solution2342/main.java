package solution2342;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.StringTokenizer;

class Main {
    static FastReader scan = new FastReader();
    static StringBuilder sb = new StringBuilder();
    static ArrayList<Integer> instructions = new ArrayList<>();
    static int[][][] cache;
    static int[][] dir = {
            {0,2,2,2,2},
            {0,1,3,4,3},
            {0,3,1,3,4},
            {0,4,3,1,3},
            {0,3,4,3,1}
    };
    public static void main(String[] args) {
        input();
        cache = new int[instructions.size()+1][5][5];
        for(int i = 0; i < instructions.size()+1; i++){
            for(int j = 0; j < 5; j++){
                for(int k = 0; k < 5; k++){
                    cache[i][j][k] = Integer.MAX_VALUE;
                }
            }
        }
        cache[0][0][0] = 0 ;

        System.out.println(solution());
    }


    static int solution(){
        for(int idx = 0; idx < instructions.size(); idx++){
            int next = instructions.get(idx);
            for(int l = 0; l < 5; l++){
                for(int r = 0; r < 5; r++){
                    int now = cache[idx][l][r];
                    if(now == Integer.MAX_VALUE)continue;
                    if(next != r){
                        // left를 next로 옮기는 경우
                        cache[idx+1][next][r] = Math.min(cache[idx+1][next][r], now + dir[l][next]);
                    }
                    if(next != l){
                        //right를 next로 옮기는 경우
                        cache[idx+1][l][next] = Math.min(cache[idx+1][l][next], now + dir[r][next]);
                    }
                }
            }
        }
        int ret = Integer.MAX_VALUE;
        for(int l = 0; l < 5; l++){
            for(int r = 0; r < 5; r++){
                ret = Math.min(ret, cache[instructions.size()-1][l][r]);
            }
        }

        return ret;
    }

    static int solutionTopDown(int idx, int l, int r){
        if (idx == instructions.size())return 0;
        int ret = cache[idx][l][r];
        if (ret!=0)return ret;
        ret = Integer.MAX_VALUE;
        if(instructions.get(idx)!=r){
            int moveLeftCost = solutionTopDown(idx + 1, instructions.get(idx), r) + dir[l][instructions.get(idx)];
            if (moveLeftCost < ret)ret = moveLeftCost;
        }
        if(instructions.get(idx)!=l){
            int moveRightCost = solutionTopDown(idx + 1, l, instructions.get(idx)) + dir[r][instructions.get(idx)];
            if (moveRightCost < ret)ret = moveRightCost;
        }
        cache[idx][l][r] = ret;

        return ret;
    }

    static void input(){
        while(true){
            int n = scan.nextInt();
            if(n==0) break;
            instructions.add(n);
        }

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