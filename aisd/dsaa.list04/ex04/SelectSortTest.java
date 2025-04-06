package dsaa.list04.ex04;

import org.junit.jupiter.api.Test;

import static dsaa.util.Common.captureOutput;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;

public class SelectSortTest {
    @Test
    void testSelectSortDescending() {
        final int[] input = {76, 71, 5, 57, 12, 50, 20, 3, 20, 55, 62, 53};
        final String[] outputLines = captureOutput(() -> SelectSort.sort(input));
        final String[] expectedSteps = {
                "76 71 5 57 12 50 20 3 20 55 62 53",
                "76 71 5 57 12 50 20 53 20 55 62 3",
                "76 71 62 57 12 50 20 53 20 55 5 3",
                "76 71 62 57 55 50 20 53 20 12 5 3",
                "76 71 62 57 55 50 20 53 20 12 5 3",
                "76 71 62 57 55 50 53 20 20 12 5 3",
                "76 71 62 57 55 53 50 20 20 12 5 3",
                "76 71 62 57 55 53 50 20 20 12 5 3",
                "76 71 62 57 55 53 50 20 20 12 5 3",
                "76 71 62 57 55 53 50 20 20 12 5 3",
                "76 71 62 57 55 53 50 20 20 12 5 3",
                "76 71 62 57 55 53 50 20 20 12 5 3",
        };
        assertArrayEquals(expectedSteps, outputLines);
    }
}
