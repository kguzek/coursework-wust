package dsaa.lab11;

import java.util.*;
import java.util.Map.Entry;

@SuppressWarnings("DuplicatedCode")
public class Graph2 {
    private static final int INFINITY = -1;
    int[][] arr;
    // Collection to map Document to index of vertex
    HashMap<String, Integer> name2Int;
    // Collection to map index of vertex to Document
    Entry<String, Document>[] arrDoc;

    // The argument type depends on a selected collection in the Main class
    @SuppressWarnings("unchecked")
    public Graph2(SortedMap<String, Document> internet) {
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

    private void updateDistance(int vertex, int lastVertex, int[] distances, int[] lastVertexes) {
        if (vertex == lastVertex) {
            return;
        }
        int weight = arr[vertex][lastVertex];
        if (weight == INFINITY) {
            return;
        }
        int distanceToLast = distances[lastVertex];
        int newDistance = distanceToLast == Integer.MAX_VALUE ? weight : distanceToLast + weight;
        if (newDistance < distances[vertex]) {
            distances[vertex] = newDistance;
            lastVertexes[vertex] = lastVertex;
        }
    }

    private void findMinimumDistances(int[] distances, int[] lastVertexes, boolean[] seenVertexes) {
        int minimumDistance = Integer.MAX_VALUE;
        int minimumIndex = INFINITY;
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < arr.length; j++) {
                if (distances[j] < minimumDistance && !seenVertexes[j]) {
                    minimumDistance = distances[j];
                    minimumIndex = j;
                }
            }
            if (minimumDistance == Integer.MAX_VALUE) {
                break;
            }
            seenVertexes[minimumIndex] = true;

            for (int j = 0; j < arr.length; j++) {
                if (!seenVertexes[j]) {
                    updateDistance(j, minimumIndex, distances, lastVertexes);
                }
            }
        }
    }

    public String DijkstraSSSP(String startVertexStr) {
        Integer startVertex = name2Int.get(startVertexStr);
        if (startVertex == null) {
            return null;
        }
        boolean[] seenVertexes = new boolean[arr.length];
        int[] distances = new int[arr.length];
        int[] lastVertexes = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            distances[i] = Integer.MAX_VALUE;
            lastVertexes[i] = INFINITY;
        }
        distances[startVertex] = 0;
        findMinimumDistances(distances, lastVertexes, seenVertexes);
        return stringifyDistances(startVertex, startVertexStr, distances, lastVertexes);
    }

    private String stringifyDistances(int startVertex, String startVertexStr, int[] distances, int[] lastVertexes) {
        StringBuilder bob = new StringBuilder();
        Stack<String> stack = new Stack<>();
        for (int i = 0; i < arr.length; i++) {
            int distance = distances[i];
            if (distance == Integer.MAX_VALUE) {
                String targetStr = arrDoc[i].getKey();
                bob.append("no path to ").append(targetStr).append('\n');
                continue;
            }
            int lastVertex = i;
            while (lastVertex != startVertex) {
                String label = arrDoc[lastVertex].getKey();
                stack.push(label);
                lastVertex = lastVertexes[lastVertex];
            }
            bob.append(startVertexStr);
            while (!stack.isEmpty()) {
                String label = stack.pop();
                bob.append("->").append(label);
            }
            bob.append("=").append(distance).append('\n');
        }
        return bob.toString();
    }
}