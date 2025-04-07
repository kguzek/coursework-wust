package dsaa.list04.ex06;

import dsaa.list02.ex02.OneWayLinkedListWithHead;
import dsaa.util.IList;
import org.junit.jupiter.api.Test;

import static dsaa.util.Common.captureOutput;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;

public class ShakerSortTest {
    private IList<Integer> arrayToList(int[] input) {
        final IList<Integer> inputList = new OneWayLinkedListWithHead<>();
        for (int element : input) {
            inputList.add(element);
        }
        return inputList;
    }

    @Test
    void testShakerSortDescending() {
        final int[] input = {76, 20, 5, 57, 12, 50, 20, 93, 44, 55, 62, 3};
        final IList<Integer> inputList = arrayToList(input);
        final ShakerSort<Integer> shaker = new ShakerSort<>(Integer::compareTo);
        final String[] outputLines = captureOutput(() -> shaker.sort(inputList));
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
        final IList<Integer> inputList = arrayToList(input);
        final ShakerSort<Integer> shaker = new ShakerSort<>(Integer::compareTo, true);
        final String[] outputLines = captureOutput(() -> shaker.sort(inputList));
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
