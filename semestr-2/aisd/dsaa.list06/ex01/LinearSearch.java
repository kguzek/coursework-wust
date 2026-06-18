package dsaa.list06.ex01;

import dsaa.util.IList;

import java.util.Comparator;
import java.util.Iterator;

public class LinearSearch<T> {
    /**
     * Zwraca pozycję znalezionego elementu. Jeśli elementu nie ma, zwraca -1.
     */
    public int linearSearch(IList<T> list, Comparator<T> comp, T what) {
        Iterator<T> it = list.iterator();
        for (int i = 0; it.hasNext(); i++) {
            if (comp.compare(what, it.next()) == 0)
                return i;
        }
        return -1;
    }
}