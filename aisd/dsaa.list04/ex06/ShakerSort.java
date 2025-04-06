package dsaa.list04.ex06;

import static dsaa.util.Common.showArray;

public class ShakerSort {
    private boolean swapped = false;
    private final boolean optimized;

    public ShakerSort() {
        this(false);
    }

    public ShakerSort(boolean optimized) {
        this.optimized = optimized;
    }

    private void trySwap(int[] arr, int idx) {
        if (arr[idx] > arr[idx - 1]) {
            int temp = arr[idx];
            arr[idx] = arr[idx - 1];
            arr[idx - 1] = temp;
            swapped = true;
        }
    }

    public void sort(int[] arr) {
        showArray(arr);
        for (int i = 0; i < arr.length - 1; i++) {
            swapped = false;
            int lastIndex = arr.length - 1;
            if (optimized) {
                lastIndex -= i;
            }
            for (int j = lastIndex; j > i; j--) {
                trySwap(arr, j);
            }
            if (optimized && !swapped) {
                break;
            }
            for (int j = i + 2; j < lastIndex; j++) {
                trySwap(arr, j);
            }
            if (optimized && !swapped) {
                break;
            }
            showArray(arr);
        }
    }
}
