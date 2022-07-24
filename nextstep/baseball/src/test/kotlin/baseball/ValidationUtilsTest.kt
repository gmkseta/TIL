package baseball

import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class ValidationUtilsTest {
    @Test
    fun 야구_숫자_1_9_검증(){
        assertTrue(ValidationUtils.validNo(9))
        assertTrue(ValidationUtils.validNo(1))
        assertFalse(ValidationUtils.validNo(0))
        assertFalse(ValidationUtils.validNo(10))
    }
}