package dsaa.list04.ex09;

import dsaa.list02.ex02.OneWayLinkedListWithHead;
import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.Arrays;
import java.util.Random;

import static dsaa.util.Common.listToArray;

public class BogoSortExperiment {
    private static final Random r = new Random();
    private static final int TARGET_SORT_TIME = 60_000;

    private static IList<Integer> generateRandomList(int length) {
        final int upperBound = Math.max(length, 100);
        IList<Integer> list = new OneWayLinkedListWithHead<>();
        for (int i = 0; i < length; i++) {
            list.add(r.nextInt(upperBound));
        }
        return list;
    }

    private static String listToString(IList<Integer> list) {
        return Arrays.toString(listToArray(list));
    }

    /**
     * Returns the average time in milliseconds that it takes to sort this array over the given number of iterations.
     */
    @SuppressWarnings("SameParameterValue")
    private static long timeToSort(IList<Integer> list) {
        ListSorter<Integer> sorter = new BogoSort<>(Integer::compareTo);
        final long startTime = System.nanoTime();
        IList<Integer> sorted = sorter.sort(list);
        final long endTime = System.nanoTime();
        System.out.println("Sorted array: " + listToString(sorted));
        return (endTime - startTime) / 1_000_000;
    }

    public static void main(String[] args) {
        float lastTime = 0;
        for (int i = 5; lastTime < TARGET_SORT_TIME; i++) {
            IList<Integer> list = generateRandomList(i);
            System.out.println("Sorting array: " + listToString(list) + "...");
            lastTime = timeToSort(list);
            System.out.printf("Average time to sort array with %d elements: %.1f s%n", i, lastTime / 1000);
        }
    }
}
