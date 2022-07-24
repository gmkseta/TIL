package baseball

class Balls(answers: Array<Int>) {
    var answers = ArrayList<Ball>();
    init {
        this.answers = arrayToBall(answers)

    }

    fun play(userBalls: Array<Int>): PlayResult {
        val userBalls = Balls(userBalls)
        var result = PlayResult()

        for(answer in answers){
            val status = userBalls.play(answer)
            result.report(status)
        }
        return result
    }

    fun play(ball: Ball): BallStatus {
        return answers.stream()
            .map{ans -> ans.play(ball)}
            .filter(BallStatus::isNotNothing)
            .findFirst()
            .orElse(BallStatus.NOTHING)
    }

    companion object {
        fun arrayToBall(answers: Array<Int>): ArrayList<Ball> {
           var balls = ArrayList<Ball>();
           for (i in 0..2) {
               balls.add(Ball(i + 1, answers[i]))
           }
           return balls
       }
    }

}
