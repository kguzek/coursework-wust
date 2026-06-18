package dsaa.list06.ex01;

import dsaa.lab07.IList;

import java.util.Comparator;
import java.util.ListIterator;

public class BinaryLinkedListSearch<T> {
    public int binaryLinkedListSearch(IList<T> list, Comparator<T> comp, T what) {
        int left = 0;
        int right = list.size() - 1;
        int middle;
        int currentPosition = 0;
        T middleValue = null;
        ListIterator<T> iterator = list.listIterator();
        while (left <= right) {
            middle = (left + right) / 2;
            while (middle > currentPosition) {
                middleValue = iterator.next();
                currentPosition++;
            }
            while (middle < currentPosition) {
                middleValue = iterator.previous();
                currentPosition--;
            }
            int compValue = comp.compare(what, middleValue);
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
