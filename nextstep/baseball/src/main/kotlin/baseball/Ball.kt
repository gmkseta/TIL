package baseball

class Ball(val position: Int, private val ballNo: Int) {


    fun play(ball: Ball): BallStatus {
        if(this == ball){
            return BallStatus.STRIKE;
        }
        if (ball.matchBallNo(ballNo)){
            return BallStatus.BALL;
        }
        return BallStatus.NOTHING;
    }

    private fun matchBallNo(ballNo: Int): Boolean {
        return this.ballNo == ballNo
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as Ball

        if (position != other.position) return false
        if (ballNo != other.ballNo) return false

        return true
    }

    override fun hashCode(): Int {
        var result = position
        result = 31 * result + ballNo
        return result
    }


}
