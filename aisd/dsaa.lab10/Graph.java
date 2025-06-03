package dsaa.lab10;

import java.util.*;
import java.util.Map.Entry;

public class Graph {
    int[][] arr;
    // Collection to map Document to index of vertex
    HashMap<String, Integer> name2Int;
    // Collection to map index of vertex to Document
    Entry<String, Document>[] arrDoc;
    DisjointSetForest forest;

    // The argument type depends on a selected collection in the Main class
    @SuppressWarnings("unchecked")
    public Graph(SortedMap<String, Document> internet) {
        int size = internet.size();
        arr = new int[size][size];
        name2Int = new HashMap<>();
        arrDoc = (Entry<String, Document>[]) new Entry[size];
        forest = new DisjointSetForest(size);
        Set<Entry<String, Document>> entries = internet.entrySet();
        Iterator<Entry<String, Document>> it = entries.iterator();
        for (int i = 0; it.hasNext(); i++) {
            Entry<String, Document> entry = it.next();
            arrDoc[i] = entry;
            name2Int.put(entry.getKey(), i);
            forest.makeSet(i);
            for (int j = 0; j < arr.length; j++) {
                arr[j][i] = -1;
            }
        }
        it = entries.iterator();
        for (int i = 0; it.hasNext(); i++) {
            Entry<String, Document> entry = it.next();
            Document doc = entry.getValue();
            for (Link link : doc.link.values()) {
                int index = name2Int.get(link.ref);
                arr[index][i] = link.weight;
                forest.union(i, index);
            }
        }
    }

    public String bfs(String start) {
        StringBuilder bob = new StringBuilder();
        bob.append(start);
        Queue<String> queue = new PriorityQueue<>();
        queue.add(start);
        while (!queue.isEmpty()) {
            int idx = name2Int.get(queue.remove());
            Document doc = arrDoc[idx].getValue();
            for (Link link : doc.link.values()) {
                bob.append(", ").append(link.ref);
                queue.add(link.ref);
            }
        }
        return bob.toString();
    }

    private void recurseNodesDfs(StringBuilder bob, String name) {
        int idx = name2Int.get(name);
        Document doc = arrDoc[idx].getValue();
        bob.append(name);
        for (Link link : doc.link.values()) {
            bob.append(", ");
            recurseNodesDfs(bob, link.ref);
        }
    }

    public String dfs(String start) {
        StringBuilder bob = new StringBuilder();
        recurseNodesDfs(bob, start);
        return bob.toString();
    }

    public int connectedComponents() {
        return forest.countSets();
    }
}
