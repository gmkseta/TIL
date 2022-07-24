package baseball

import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.Test

class BallsTest {

    @Test
    fun play(){
        val ans = Balls(arrayOf(1,2,3))
        val result: PlayResult = ans.play(arrayOf(4,5,6))

        result.getStrike() shouldBe 0

        result.getBall() shouldBe 0
    }

    @Test
    fun play_1strike_1ball(){
        val ans = Balls(arrayOf(1,2,3))
        val result: PlayResult = ans.play(arrayOf(1,4,2))
        result.getStrike() shouldBe 1
        result.getBall() shouldBe 1
    }

    @Test
    fun play_3strike(){
        val ans = Balls(arrayOf(1,2,3))
        val result: PlayResult = ans.play(arrayOf(1,2,2))
        result.isGameEnd() shouldBe true
    }

    @Test
    fun nothing(){
        val ans = Balls(arrayOf(1,2,3))

        val status = ans.play(Ball(1, 4))

        status shouldBe BallStatus.NOTHING

    }

    @Test
    fun ball(){
        val ans = Balls(arrayOf(1,2,3))

        val status = ans.play(Ball(1, 2))

        status shouldBe BallStatus.BALL
    }

    @Test
    fun strike(){
        val ans = Balls(arrayOf(1,2,3))

        val status = ans.play(Ball(1, 1))

        status shouldBe BallStatus.STRIKE
    }

}