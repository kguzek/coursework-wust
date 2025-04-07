package dsaa.list04.ex05;

import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.Comparator;

import static dsaa.util.Common.listToString;

public class BubbleSort<T> implements ListSorter<T> {
    private final Comparator<T> _comparator;

    public BubbleSort(Comparator<T> comparator) {
        _comparator = comparator;
    }

    public IList<T> sort(IList<T> list) {
        System.out.println(listToString(list));
        for (int i = 0; i < list.size() - 1; i++) {
            T right = list.get(list.size() - 1);
            for (int j = list.size() - 2; j >= i; j--) {
                T left = list.get(j);
                if (_comparator.compare(right, left) > 0) {
                    list.set(j + 1, left);
                    list.set(j, right);
                } else {
                    right = left;
                }
            }
            System.out.println(listToString(list));
        }
        return list;
    }
}
