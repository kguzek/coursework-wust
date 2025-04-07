package dsaa.list04.ex05;

import dsaa.util.IList;
import dsaa.util.ListSorter;
import org.junit.jupiter.api.Test;

import static dsaa.util.Common.arrayToList;
import static dsaa.util.Common.captureOutput;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;

public class BubbleSortTest {
    private final ListSorter<Integer> sorter = new BubbleSort<>(Integer::compareTo);

    @Test
    void testBubbleSortDescending() {
        final int[] input = {76, 20, 5, 57, 12, 50, 20, 93, 44, 55, 62, 3};
        final IList<Integer> inputList = arrayToList(input);
        final String[] outputLines = captureOutput(() -> sorter.sort(inputList));
        final String[] expectedSteps = {
                "[76, 20, 5, 57, 12, 50, 20, 93, 44, 55, 62, 3]",
                "[93, 76, 20, 5, 57, 12, 50, 20, 62, 44, 55, 3]",
                "[93, 76, 62, 20, 5, 57, 12, 50, 20, 55, 44, 3]",
                "[93, 76, 62, 57, 20, 5, 55, 12, 50, 20, 44, 3]",
                "[93, 76, 62, 57, 55, 20, 5, 50, 12, 44, 20, 3]",
                "[93, 76, 62, 57, 55, 50, 20, 5, 44, 12, 20, 3]",
                "[93, 76, 62, 57, 55, 50, 44, 20, 5, 20, 12, 3]",
                "[93, 76, 62, 57, 55, 50, 44, 20, 20, 5, 12, 3]",
                "[93, 76, 62, 57, 55, 50, 44, 20, 20, 12, 5, 3]",
                "[93, 76, 62, 57, 55, 50, 44, 20, 20, 12, 5, 3]",
                "[93, 76, 62, 57, 55, 50, 44, 20, 20, 12, 5, 3]",
                "[93, 76, 62, 57, 55, 50, 44, 20, 20, 12, 5, 3]",
        };
        assertArrayEquals(expectedSteps, outputLines);
    }
}
