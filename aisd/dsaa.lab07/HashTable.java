package dsaa.lab07;

import java.util.LinkedList;

public class HashTable {
    private final static int defaultInitSize = 8;
    private final static double defaultMaxLoadFactor = 0.7;
    private final double maxLoadFactor;
    LinkedList[] arr; // use pure array
    private int size;

    public HashTable() {
        this(defaultInitSize);
    }

    public HashTable(int size) {
        this(size, defaultMaxLoadFactor);
    }


    public HashTable(int initCapacity, double maxLF) {
        //TODO
        this.maxLoadFactor = maxLF;
    }

    public boolean add(Object elem) {
        //TODO
        return true;
    }


    private void doubleArray() {
        //TODO
    }


    @Override
    public String toString() {
        //TODO
        // use	IWithName x=(IWithName)elem;
        return null;
    }

    public Object get(Object toFind) {
        //TODO
        return null;
    }

}

