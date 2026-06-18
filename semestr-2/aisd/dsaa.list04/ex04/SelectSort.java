package dsaa.list04.ex04;

import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.Comparator;
import java.util.Iterator;
import java.util.ListIterator;

import static dsaa.util.Common.listToString;

public class SelectSort<T> implements ListSorter<T> {
    private final Comparator<T> _comparator;

    public SelectSort(Comparator<T> comparator) {
        _comparator = comparator;
    }

    public IList<T> sort(IList<T> list) {
        System.out.println(listToString(list));
        if (list.isEmpty()) {
            return list;
        }
        ListIterator<T> itOuter = list.listIterator();
        while (itOuter.hasNext()) {
            itOuter.next();
        }
        for (int i = list.size() - 1; i > 0; i--) {
            T valueOuter = itOuter.previous();
            int minIndex = 0;
            Iterator<T> it = list.iterator();
            T minValue = it.next();
            for (int j = 1; j <= i; j++) {
                T currentValue = it.next();
                if (_comparator.compare(currentValue, minValue) < 0) {
                    minIndex = j;
                    minValue = currentValue;
                }
            }
            if (minIndex != i) {
                list.set(minIndex, valueOuter);
                itOuter.set(minValue);
            }
            System.out.println(listToString(list));
        }
        return list;
    }
}
