package dsaa.lab11;

import java.util.*;
import java.util.Map.Entry;

@SuppressWarnings("DuplicatedCode")
public class Graph {
    private static final int INFINITY = -1;
    int[][] arr;
    // Collection to map Document to index of vertex
    HashMap<String, Integer> name2Int;
    // Collection to map index of vertex to Document
    Entry<String, Document>[] arrDoc;

    // The argument type depends on a selected collection in the Main class
    @SuppressWarnings("unchecked")
    public Graph(SortedMap<String, Document> internet) {
        int size = internet.size();
        arr = new int[size][size];
        name2Int = new HashMap<>();
        arrDoc = (Entry<String, Document>[]) new Entry[size];
        Set<Entry<String, Document>> entries = internet.entrySet();
        Iterator<Entry<String, Document>> it = entries.iterator();
        for (int i = 0; it.hasNext(); i++) {
            Entry<String, Document> entry = it.next();
            arrDoc[i] = entry;
            name2Int.put(entry.getKey(), i);
            for (int j = 0; j < arr.length; j++) {
                arr[j][i] = INFINITY;
            }
        }
        it = entries.iterator();
        for (int i = 0; it.hasNext(); i++) {
            Entry<String, Document> entry = it.next();
            Document doc = entry.getValue();
            for (Link link : doc.link.values()) {
                Integer index = name2Int.get(link.ref);
                if (index == null) {
                    continue;
                }
                arr[index][i] = link.weight;
            }
        }
    }

    public String bfs(String start) {
        StringBuilder bob = new StringBuilder();
        bob.append(start);
        Queue<String> queue = new PriorityQueue<>();
        Set<String> seenNames = new HashSet<>();
        seenNames.add(start);
        queue.add(start);
        while (!queue.isEmpty()) {
            String name = queue.remove();
            Integer idx = name2Int.get(name);
            if (idx == null) {
                return null;
            }
            Document doc = arrDoc[idx].getValue();
            for (Link link : doc.link.values()) {
                if (seenNames.add(link.ref)) {
                    bob.append(", ").append(link.ref);
                    queue.add(link.ref);
                }
            }
        }
        return bob.toString();
    }

    private void recurseNodesDfs(StringBuilder bob, Set<String> seenNames, String name) throws NoSuchElementException {
        Integer idx = name2Int.get(name);
        if (idx == null) {
            throw new NoSuchElementException(name);
        }
        Document doc = arrDoc[idx].getValue();
        bob.append(name);
        for (Link link : doc.link.values()) {
            if (seenNames.add(link.ref)) {
                bob.append(", ");
                recurseNodesDfs(bob, seenNames, link.ref);
            }
        }
    }

    public String dfs(String start) {
        StringBuilder bob = new StringBuilder();
        Set<String> seenNames = new HashSet<>();
        seenNames.add(start);
        try {
            recurseNodesDfs(bob, seenNames, start);
        } catch (NoSuchElementException e) {
            return null;
        }
        return bob.toString();
    }

    public int connectedComponents() {
        DisjointSetForest forest = new DisjointSetForest(arr.length);
        for (int i = 0; i < arr.length; i++) {
            forest.makeSet(i);
        }
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr.length; j++) {
                if (arr[i][j] != INFINITY) {
                    forest.union(i, j);
                }
            }
        }
        return forest.countSets();
    }

    public String DijkstraSSSP(String startVertexStr) {
        // TODO: implement this
        return null;
    }
}