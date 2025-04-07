package dsaa.list04.ex03;

import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.Comparator;
import java.util.ListIterator;

import static dsaa.util.Common.listToString;

public class InsertSort<T> implements ListSorter<T> {
    private final Comparator<T> _comparator;

    public InsertSort(Comparator<T> comparator) {
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
        itOuter.previous();
        for (int i = list.size() - 2; itOuter.hasPrevious(); i--) {
            T current = itOuter.previous();
            int newIndex;
            for (newIndex = i; newIndex < list.size() - 1; newIndex++) {
                if (_comparator.compare(current, list.get(newIndex + 1)) > 0) {
                    break;
                }
            }
            if (newIndex != i) {
                itOuter.remove();
                list.add(newIndex, current);
            }
            System.out.println(listToString(list));
        }
        return list;
    }
}
