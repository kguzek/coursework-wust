package dsaa.list04.ex03;

import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.Comparator;
import java.util.Iterator;
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
            Iterator<T> itInner = list.iterator();
            for (int j = 0; j <= i; j++) {
                itInner.next();
            }
            int newIndex = i;
            while (itInner.hasNext()) {
                if (_comparator.compare(current, itInner.next()) > 0) {
                    break;
                }
                newIndex++;
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
