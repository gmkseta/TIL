package baseball

enum class BallStatus {
    NOTHING,
    BALL,
    STRIKE;

    fun isNotNothing(): Boolean {
        return this != NOTHING
    }

    fun isStrike(): Boolean {
        return this == STRIKE
    }

    fun isBall(): Boolean {
        return this == BALL
    }

}
