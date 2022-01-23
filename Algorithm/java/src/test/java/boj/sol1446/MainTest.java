package boj.sol1446;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import static org.junit.jupiter.api.Assertions.*;

class MainTest {

    @ParameterizedTest
    @MethodSource("solutionParams")
    void solution(int N, int D, int[][] road, int ans) {
        Main sol = new Main();
        int actual = sol.solution(N, D, road);
        Assertions.assertEquals(ans, actual);
    }

    private static Object[] solutionParams() {
        return new Object[]{
                new Object[]{5, 150, new int[][]{
                        new int[]{0, 50, 10},
                        new int[]{0, 50, 20},
                        new int[]{50, 100, 10},
                        new int[]{100, 151, 10},
                        new int[]{110, 140, 90}
                }, 70},
                new Object[]{2, 100, new int[][]{new int[]{10, 60, 40}, new int[]{50, 90, 20}}, 80},
                new Object[]{8, 900, new int[][]{
                        new int[]{0, 10, 9},
                        new int[]{20, 60, 45},
                        new int[]{80, 190, 100},
                        new int[]{50, 70, 15},
                        new int[]{160, 180, 14},
                        new int[]{140, 160, 14},
                        new int[]{420, 901, 5},
                        new int[]{450, 900, 0}
                }, 432},
        };
    }
}