package dsaa.list04.ex04;

import static dsaa.util.Common.showArray;

public class SelectSort {
    @SuppressWarnings("DuplicatedCode")
    public static void sort(int[] arr) {
        showArray(arr);
        for (int i = arr.length - 1; i > 0; i--) {
            int minIndex = 0;
            for (int j = 1; j <= i; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex != i) {
                int minValue = arr[minIndex];
                System.arraycopy(arr, minIndex + 1, arr, minIndex, i - minIndex);
                arr[i] = minValue;
            }
            showArray(arr);
        }
    }
}
