package dsaa.list04.ex06;

import org.junit.jupiter.api.Test;

import static dsaa.util.Common.captureOutput;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;

public class ShakerSortTest {
    @Test
    void testShakerSortDescending() {
        final int[] input = {76, 20, 5, 57, 12, 50, 20, 93, 44, 55, 62, 3};
        final ShakerSort shaker = new ShakerSort();
        final String[] outputLines = captureOutput(() -> shaker.sort(input));
        final String[] expectedSteps = {
                "76 20 5 57 12 50 20 93 44 55 62 3",
                "93 76 20 57 12 50 20 62 44 55 5 3",
                "93 76 62 57 20 50 20 55 44 12 5 3",
                "93 76 62 57 55 50 20 44 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
        };
        assertArrayEquals(expectedSteps, outputLines);
    }


    @Test
    void testShakerSortDescendingOptimized() {
        final int[] input = {76, 20, 5, 57, 12, 50, 20, 93, 44, 55, 62, 3};
        final ShakerSort shaker = new ShakerSort(true);
        final String[] outputLines = captureOutput(() -> shaker.sort(input));
        final String[] expectedSteps = {
                "76 20 5 57 12 50 20 93 44 55 62 3",
                "93 76 20 57 12 50 20 62 44 55 5 3",
                "93 76 62 57 20 50 20 55 44 12 5 3",
                "93 76 62 57 55 50 20 44 20 12 5 3",
                "93 76 62 57 55 50 44 20 20 12 5 3",
        };
        assertArrayEquals(expectedSteps, outputLines);
    }
}
