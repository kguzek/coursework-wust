package dsaa.list06.ex01;

import dsaa.util.IList;

import java.util.Comparator;

public class BinarySearch<T> {
    public int binarySearch(IList<T> list, Comparator<T> comp, T what) {
        int left = 0;
        int right = list.size() - 1;
        int middle;
        while (left <= right) {
            middle = (left + right) / 2;
            int compValue = comp.compare(what, list.get(middle));
            if (compValue == 0)
                return middle;
            if (compValue < 0)
                right = middle - 1;
            else
                left = middle + 1;
        }
        return -1;
    }
}
