import camp.nextstep.edu.missionutils.test.Assertions.assertRandomNumberInRangeTest
import camp.nextstep.edu.missionutils.test.Assertions.assertSimpleTest
import camp.nextstep.edu.missionutils.test.NsTest
import io.kotest.matchers.collections.shouldBeIn
import org.assertj.core.api.Assertions.assertThatThrownBy
import org.junit.jupiter.api.Test

internal class MainKtTest: NsTest() {


    @Test
    fun 게임종료_후_재시작(){
        assertRandomNumberInRangeTest(
            {
                run("246", "135", "1", "597", "589", "2")
                print(output())
                output().shouldBeIn("낫싱", "3스트라이크", "1볼 1스트라이크", "3스트라이크", "게임 종료")
            },
            1, 3, 5, 5, 8, 9
        )
    }

    @Test
    fun 예외_테스트() {
        assertSimpleTest {
            assertThatThrownBy { runException("1234") }
                .isInstanceOf(IllegalArgumentException::class.java)
        }
    }

    override fun runMain() {
        main(arrayOf<String>())
    }

}