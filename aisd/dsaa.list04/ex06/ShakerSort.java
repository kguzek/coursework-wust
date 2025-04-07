package dsaa.list04.ex06;

import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.Comparator;

import static dsaa.util.Common.listToString;

public class ShakerSort<T> implements ListSorter<T> {
    private final Comparator<T> _comparator;
    private final boolean optimized;
    private boolean swapped = false;

    public ShakerSort(Comparator<T> comparator) {
        this(comparator, false);
    }

    public ShakerSort(Comparator<T> comparator, boolean optimized) {
        this._comparator = comparator;
        this.optimized = optimized;
    }

    private void trySwap(IList<T> list, int idx) {
        T left = list.get(idx - 1);
        T right = list.get(idx);
        if (_comparator.compare(left, right) < 0) {
            list.set(idx, left);
            list.set(idx - 1, right);
            swapped = true;
        }
    }

    public IList<T> sort(IList<T> list) {
        System.out.println(listToString(list));
        for (int i = 0; i < list.size(); i++) {
            swapped = false;
            int lastIndex = list.size() - 1;
            if (optimized) {
                lastIndex -= i;
            }
            for (int j = lastIndex; j > i; j--) {
                trySwap(list, j);
            }
            if (optimized && !swapped) {
                break;
            }
            for (int j = i + 2; j < lastIndex; j++) {
                trySwap(list, j);
            }
            if (optimized && !swapped) {
                break;
            }
            System.out.println(listToString(list));
        }
        return list;
    }
}
