package dsaa.list04.ex09;

import dsaa.list02.ex02.OneWayLinkedListWithHead;
import dsaa.util.IList;
import dsaa.util.ListSorter;

import java.util.*;


public class BogoSort<T> implements ListSorter<T> {
    private final Comparator<T> _comparator;

    public BogoSort(Comparator<T> comparator) {
        _comparator = comparator;
    }

    public IList<T> sort(IList<T> list) {
        IList<T> sortedList = list;
        while (!isSorted(sortedList)) {
            sortedList = shuffle(list);
        }
        return sortedList;
    }

    private IList<T> shuffle(IList<T> list) {
        IList<T> shuffledList = new OneWayLinkedListWithHead<>();
        int size = list.size();
        if (size <= 1) return list;

        List<T> tempList = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            tempList.add(list.get(i));
        }

        Collections.shuffle(tempList);
        for (T item : tempList) {
            shuffledList.add(item);
        }
        return shuffledList;
    }

    private boolean isSorted(IList<T> list) {
        if (list.isEmpty()) {
            return true;
        }
        Iterator<T> it = list.iterator();
        T first = it.next();
        while (it.hasNext()) {
            T second = it.next();
            if (_comparator.compare(first, second) > 0) {
                return false;
            }
            first = second;
        }
        return true;
    }
}
