package baseball

class PlayResult {
    private var strike = 0
    private var ball = 0

    fun getStrike(): Int{
        return strike
    }
    fun getBall(): Int{
        return ball
    }

    fun  report(ballStatus: BallStatus) {
        if(ballStatus.isStrike()){
            strike++;
        }
        if(ballStatus.isBall()){
            ball++;
        }

    }

    fun isGameEnd(): Boolean {
        return strike == 3
    }

}
