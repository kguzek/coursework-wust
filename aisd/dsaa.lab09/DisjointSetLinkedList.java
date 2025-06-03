package dsaa.lab09;

public class DisjointSetLinkedList implements DisjointSetDataStructure {

    private static final int NULL = -1;
    Element[] arr;

    public DisjointSetLinkedList(int size) {
        arr = new Element[size];
    }

    @Override
    public void makeSet(int item) {
        Element e = new Element();
        e.representative = item;
        e.next = NULL;
        e.length = 1;
        e.last = item;
        arr[item] = e;
    }

    @Override
    public int findSet(int item) {
        return arr[item].representative;
    }

    @Override
    public boolean union(int itemA, int itemB) {
        int repA = findSet(itemA);
        int repB = findSet(itemB);
        if (repA == NULL || repB == NULL || repA == repB) {
            return false;
        }
        if (arr[repB].length > arr[repA].length) {
            int temp = repB;
            repB = repA;
            repA = temp;
        }
        arr[repA].length += arr[repB].length;
        for (int i = repB; i != NULL; i = arr[i].next) {
            arr[i].representative = repA;
            arr[i].length = 0;
        }
        arr[arr[repA].last].next = repB;
        arr[repA].last = arr[repB].last;
        return true;
    }

    @Override
    public String toString() {
        StringBuilder bob = new StringBuilder();
        bob.append("Disjoint sets as linked list:");
        for (int i = 0; i < arr.length; i++) {
            if (arr[i].representative != i) {
                continue;
            }
            bob.append("\n").append(i);
            for (int j = arr[i].next; j != NULL; j = arr[j].next) {
                bob.append(", ").append(j);
            }
        }
        return bob.toString();
    }

    private class Element {
        int representative;
        int next;
        int length;
        int last;
    }

}
