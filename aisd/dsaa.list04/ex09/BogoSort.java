package dsaa.list04.ex09;

import java.util.Random;

public class BogoSort {
    private static final Random r = new Random();

    public static void sort(int[] arr) {
        while (!isSorted(arr)) {
            shuffle(arr);
        }
    }

    private static void shuffle(int[] arr) {
        for (int i = arr.length - 1; i > 0; i--) {
            int j = r.nextInt(i + 1);
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    private static boolean isSorted(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            if (arr[i - 1] > arr[i]) {
                return false;
            }
        }
        return true;
    }
}
