package dsaa.lab08;

import java.util.Iterator;
import java.util.LinkedList;

@SuppressWarnings("DuplicatedCode")
public class HashTable {
    private final static int defaultInitSize = 8;
    private final static double defaultMaxLoadFactor = 0.7;
    private final double maxLoadFactor;
    LinkedList<Object>[] arr; // use pure array
    private int capacity;
    private int size;

    @SuppressWarnings("unused")
    public HashTable() {
        this(defaultInitSize);
    }

    public HashTable(int capacity) {
        this(capacity, defaultMaxLoadFactor);
    }


    public HashTable(int initCapacity, double maxLF) {
        this.maxLoadFactor = maxLF;
        capacity = initCapacity;
        // noinspection unchecked
        arr = new LinkedList[capacity];
        for (int i = 0; i < capacity; i++) {
            arr[i] = new LinkedList<>();
        }
        size = 0;
    }

    private float getLoadFactor() {
        return (float) size / capacity;
    }

    private LinkedList<Object> getList(Object key) {
        int index = key.hashCode() % capacity;
        return arr[index];
    }

    public boolean add(Object elem) {
        LinkedList<Object> list = getList(elem);
        if (list.contains(elem)) {
            return false;
        }
        if (list.add(elem)) {
            size++;
            if (getLoadFactor() > maxLoadFactor) {
                doubleArray();
            }
            return true;
        }
        return false;
    }

    private void doubleArray() {
        capacity *= 2;
        LinkedList<Object>[] oldArr = arr;
        // noinspection unchecked
        arr = new LinkedList[capacity];
        size = 0;
        for (int i = 0; i < capacity; i++) {
            arr[i] = new LinkedList<>();
        }
        for (LinkedList<Object> list : oldArr) {
            for (Object elem : list) {
                add(elem);
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder bob = new StringBuilder();
        for (int i = 0; i < capacity; i++) {
            bob.append(i).append(":");
            Iterator<Object> it = arr[i].iterator();
            if (it.hasNext()) {
                IWithName withName = (IWithName) it.next();
                bob.append(" ").append(withName.getName());
            }
            while (it.hasNext()) {
                IWithName withName = (IWithName) it.next();
                bob.append(", ").append(withName.getName());
            }
            bob.append('\n');
        }
        return bob.toString();
    }

    public Object get(Object toFind) {
        for (Object elem : getList(toFind)) {
            if (elem.equals(toFind)) {
                return elem;
            }
        }
        return null;
    }
}

