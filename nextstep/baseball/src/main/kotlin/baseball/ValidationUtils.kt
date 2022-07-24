package baseball

private const val MIN_NO = 1

private const val MAX_NO = 9

class ValidationUtils {
    companion object {
        fun validNo(num: Int): Boolean {
            return num in MIN_NO..MAX_NO;
        }
    }

}
