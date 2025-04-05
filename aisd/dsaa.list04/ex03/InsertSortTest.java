package dsaa.list04.ex03;

import org.junit.jupiter.api.Test;

import static dsaa.util.Common.captureOutput;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;

public class InsertSortTest {

    @Test
    void testInsertSortDescending() {
        final int[] input = {3, 76, 71, 5, 57, 12, 50, 20, 93, 20, 4, 62};
        final String[] outputLines = captureOutput(() -> InsertSort.sort(input));
        final String[] expectedSteps = {
                "3 76 71 5 57 12 50 20 93 20 4 62",
                "3 76 71 5 57 12 50 20 93 20 62 4",
                "3 76 71 5 57 12 50 20 93 62 20 4",
                "3 76 71 5 57 12 50 20 93 62 20 4",
                "3 76 71 5 57 12 50 93 62 20 20 4",
                "3 76 71 5 57 12 93 62 50 20 20 4",
                "3 76 71 5 57 93 62 50 20 20 12 4",
                "3 76 71 5 93 62 57 50 20 20 12 4",
                "3 76 71 93 62 57 50 20 20 12 5 4",
                "3 76 93 71 62 57 50 20 20 12 5 4",
                "3 93 76 71 62 57 50 20 20 12 5 4",
                "93 76 71 62 57 50 20 20 12 5 4 3",
        };
        assertArrayEquals(expectedSteps, outputLines);
    }
}
