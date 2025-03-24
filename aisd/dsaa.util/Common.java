package dsaa.util;

import java.util.Iterator;

public class Common {
    @SuppressWarnings("unchecked")
    public static <E> E[] listToArray(IList<E> list) {
        E[] result = (E[]) new Object[list.size()];
        Iterator<E> it = list.iterator();
        for (int i = 0; it.hasNext(); i++) {
            result[i] = it.next();
        }
        return result;
    }
}
