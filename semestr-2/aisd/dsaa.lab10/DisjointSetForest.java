package dsaa.lab10;

import java.util.HashSet;
import java.util.Set;

@SuppressWarnings("DuplicatedCode")
public class DisjointSetForest implements DisjointSetDataStructure {

    Element[] arr;

    public DisjointSetForest(int size) {
        arr = new Element[size];
    }

    @Override
    public void makeSet(int item) {
        Element e = new Element();
        e.rank = 0;
        e.parent = item;
        arr[item] = e;
    }

    @Override
    public int findSet(int item) {
        int parent = arr[item].parent;
        if (parent == item) {
            return item;
        }
        parent = findSet(parent);
        arr[item].parent = parent;
        return parent;
    }

    @Override
    public boolean union(int itemA, int itemB) {
        int parentA = findSet(itemA);
        int parentB = findSet(itemB);
        if (parentA == parentB) {
            return false;
        }
        if (arr[parentA].rank <= arr[parentB].rank) {
            int temp = parentB;
            parentB = parentA;
            parentA = temp;
        }
        if (arr[parentA].rank == arr[parentB].rank) {
            arr[parentA].rank++;
        }
        arr[parentB].parent = parentA;
        return true;
    }

    @Override
    public String toString() {
        StringBuilder bob = new StringBuilder();
        bob.append("Disjoint sets as forest:");
        for (int i = 0; i < arr.length; i++) {
            bob.append("\n").append(i).append(" -> ").append(arr[i].parent);
        }
        return bob.toString();
    }

    @Override
    public int countSets() {
        Set<Integer> seenParents = new HashSet<>();
        for (Element element : arr) {
            seenParents.add(element.parent);
        }
        return seenParents.size();
    }

    @SuppressWarnings("InnerClassMayBeStatic")
    private class Element {
        int rank;
        int parent;
    }
}
