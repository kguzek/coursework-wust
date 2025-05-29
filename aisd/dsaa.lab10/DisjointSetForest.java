package dsaa.lab10;

public class DisjointSetForest implements DisjointSetDataStructure {

    Element[] arr;

    public DisjointSetForest(int size) {
        //TODO
    }

    @Override
    public void makeSet(int item) {
        //TODO
    }

    @Override
    public int findSet(int item) {
        //TODO
        return -1;
    }

    @Override
    public boolean union(int itemA, int itemB) {
        //TODO
        return false;
    }

    @Override
    public String toString() {
        //TODO
        return null;
    }

    @Override
    public int countSets() {
        // TODO
        return -1;
    }

    class Element {
        int rank;
        int parent;
    }
}
