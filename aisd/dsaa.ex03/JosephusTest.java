package dsaa.ex03;

import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

import java.util.Arrays;
import java.util.stream.Stream;

import static dsaa.ex03.Josephus.josephus;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class JosephusTest {
    private static final int[][] TEST_CASES = {
            {5, 2, 2},
            {7, 3, 3},
            {10, 4, 4},
            {6, 1, 5},
            {8, 5, 2},
            {12, 6, 2},
            {15, 7, 4},
            {20, 10, 2},
            {25, 12, 1},
            {30, 15, 3}
    };

    @TestFactory
    Stream<DynamicTest> testJosephus() {
        return Arrays.stream(TEST_CASES)
                .map(testCase -> DynamicTest.dynamicTest(
                        String.format("Josephus(%d, %d) should return %d", testCase[0], testCase[1], testCase[2]),
                        () -> assertEquals(testCase[2], josephus(testCase[0], testCase[1]))
                ));
    }
}
