package dsaa.list04.ex05;

import static dsaa.util.Common.showArray;

public class BubbleSort {
    @SuppressWarnings("DuplicatedCode")
    public static void sort(int[] arr) {
        showArray(arr);
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = arr.length - 1; j > i; j--) {
                if (arr[j] > arr[j - 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j - 1];
                    arr[j - 1] = temp;
                }
            }
            showArray(arr);
        }
    }
}
