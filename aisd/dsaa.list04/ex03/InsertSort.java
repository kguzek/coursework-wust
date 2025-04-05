package dsaa.list04.ex03;

import static dsaa.util.Common.showArray;

public class InsertSort {
    @SuppressWarnings("DuplicatedCode")
    public static void sort(int[] arr) {
        showArray(arr);
        for (int i = arr.length - 2; i >= 0; i--) {
            int current = arr[i];
            int newIndex;
            for (newIndex = i; newIndex < arr.length - 1; newIndex++) {
                if (current > arr[newIndex + 1]) {
                    break;
                }
            }
            if (newIndex != i) {
                // przesuwam połowę posortowanej części w lewo o jedno miejsce
                System.arraycopy(arr, i + 1, arr, i, newIndex - i);
                arr[newIndex] = current;
            }
            showArray(arr);
        }
    }
}
