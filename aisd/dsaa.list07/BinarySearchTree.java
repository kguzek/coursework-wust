package dsaa.list07;

import java.util.*;

public class BinarySearchTree<T> {
    private final Comparator<T> _comparator;
    private Node _root;

    public BinarySearchTree(Comparator<T> comp) {
        _comparator = comp;
        _root = null;
    }


    static <Y> boolean allElementsAreNull(Iterable<Y> iterable) {
        for (Y elem : iterable) {
            if (elem == null) continue;
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        printNodeInternal(Collections.singletonList(_root), 1, getHeight(), sb);
        return sb.toString();
    }

    public T find(T elem) {
        Node node = search(elem);
        return node == null ? null : node.value;
    }

    private Node search(T elem) {
        Node node = _root;
        int cmp;
        while (node != null && (cmp = _comparator.compare(elem, node.value)) != 0)
            node = cmp < 0 ? node.left : node.right;
        return node;
    }

    public <R> void inOrderWalk(IExecutor<T, R> exec) {
        inOrderWalk(_root, exec);
    }

    public void insert(T elem) throws DuplicateElementException {
        _root = insert(_root, elem);
    }

    private Node delete(T elem, Node node) {
        if (node == null) throw new NoSuchElementException();
        else {
            int cmp = _comparator.compare(elem, node.value);
            if (cmp < 0) node.left = delete(elem, node.left);
            else if (cmp > 0) node.right = delete(elem, node.right);
            else if (node.left != null && node.right != null) node.right = detachMin(node, node.right);
            else node = (node.left != null) ? node.left : node.right;
        }
        return node;
    }

    private T deleteWrapper(T elem, Node node) {
        Node deletedNode = delete(elem, node);
        return deletedNode == null ? null : deletedNode.value;
    }

    public T delete(T elem, T value) {
        return deleteWrapper(elem, search(value));
    }

    @SuppressWarnings("UnusedReturnValue")
    public T delete(T value) {
        return deleteWrapper(value, _root);
    }

    private Node detachMin(Node del, Node node) {
        if (node.left != null) node.left = detachMin(del, node.left);
        else {
            del.value = node.value;
            node = node.right;
        }
        return node;
    }

    private Node insert(Node node, T elem) throws DuplicateElementException {
        if (node == null) node = new Node(elem);
        else {
            int cmp = _comparator.compare(elem, node.value);
            if (cmp < 0) node.left = insert(node.left, elem);
            else if (cmp > 0) node.right = insert(node.right, elem);
            else throw new DuplicateElementException(elem.toString());
        }
        return node;
    }

    private <R> void inOrderWalk(Node node, IExecutor<T, R> exec) {
        if (node != null) {
            inOrderWalk(node.left, exec);
            exec.execute(node.value);
            inOrderWalk(node.right, exec);
        }
    }

    public T successor(T elem) {
        Node succNode = successorNode(_root, elem);
        return succNode == null ? null : succNode.value;
    }

    private Node successorNode(Node node, T elem) {
        if (node == null) throw new NoSuchElementException();
        int cmp = _comparator.compare(elem, node.value);
        if (cmp == 0) {
            if (node.right != null) return getMin(node.right);
            else return null;
        } else if (cmp < 0) {
            Node retNode = successorNode(node.left, elem);
            return retNode == null ? node : retNode;
        } else { // cmp>0
            return successorNode(node.right, elem);
        }
    }

    public T getMin() {
        if (_root == null) throw new NoSuchElementException();
        Node node = getMin(_root);
        return node.value;
    }

    public T getMax() {
        if (_root == null) throw new NoSuchElementException();
        Node node = getMax(_root);
        return node.value;
    }

    private Node getMin(Node node) {
        assert (node != null);
        while (node.left != null) node = node.left;
        return node;
    }

    private Node getMax(Node node) {
        assert (node != null);
        while (node.right != null) node = node.right;
        return node;
    }

    private void printNodeInternal(List<Node> nodes, int level, int maxLevel, StringBuilder sb) {
        if (nodes.isEmpty() || allElementsAreNull(nodes)) return;

        int floor = maxLevel - level;
        int edgeLines = (int) Math.pow(2, (Math.max(floor - 1, 0)));
        int firstSpaces = (int) Math.pow(2, (floor)) - 1;
        int betweenSpaces = (int) Math.pow(2, (floor + 1)) - 1;

        sb.append(" ".repeat(firstSpaces));

        List<Node> newNodes = new ArrayList<>();
        for (Node node : nodes) {
            if (node != null) {
                sb.append(node.value);
                newNodes.add(node.left);
                newNodes.add(node.right);
            } else {
                newNodes.add(null);
                newNodes.add(null);
                sb.append(" ");
            }

            sb.append(" ".repeat(betweenSpaces));
        }
        sb.append("\n");

        for (int i = 1; i <= edgeLines; i++) {
            for (Node node : nodes) {
                if (firstSpaces > i) sb.append(" ".repeat(firstSpaces - i));
                if (node == null) {
                    sb.append(" ".repeat(edgeLines + edgeLines + i + 1));
                    continue;
                }

                if (node.left != null) sb.append("/");
                else sb.append(" ");

                sb.append(" ".repeat(i * 2 - 1));

                if (node.right != null) sb.append("\\");
                else sb.append(" ");

                sb.append(" ".repeat(edgeLines + edgeLines - i));
            }

            sb.append("\n");
        }
        printNodeInternal(newNodes, level + 1, maxLevel, sb);
    }

    public int getHeight() {
        return getHeight(_root);
    }

    private int getHeight(Node node) {
        if (node == null) {
            return 0;
        }
        int leftHeight = getHeight(node.left);
        int rightHeight = getHeight(node.right);
        return Math.max(leftHeight, rightHeight) + 1;
    }


    class Node {
        T value; // element
        Node left;
        Node right;

        Node(T obj) {
            value = obj;
        }

        Node(T obj, Node leftNode, Node rightNode) {
            value = obj;
            left = leftNode;
            right = rightNode;
        }
    }
}
