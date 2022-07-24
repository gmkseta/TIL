package baseball

import io.kotest.matchers.shouldBe
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test

class BallTest {
    private lateinit var com: Ball

    @BeforeEach
    internal fun setUp() {
        com = Ball(1, 4);
    }

    @Test
    fun nothing(){
        val status = com.play(Ball(2, 5))
        status shouldBe BallStatus.NOTHING
    }

    @Test
    fun ball(){
        val status = com.play(Ball(2, 4))
        status shouldBe BallStatus.BALL
    }

    @Test
    fun strike(){
        val status = com.play(Ball(1, 4))
        status shouldBe BallStatus.STRIKE
    }
}