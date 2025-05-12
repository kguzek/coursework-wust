package dsaa.lab08;

public class BST<T> {
    private final Node root = null;

    public BST() {
    }

    public T getElement(T toFind) {
        // TODO
        return null;
    }

    public T successor(T elem) {
        // TODO
        return null;
    }

    public String toStringInOrder() {
        // TODO
        return null;
    }

    public String toStringPreOrder() {
        // TODO
        return null;
    }

    public String toStringPostOrder() {
        // TODO
        return null;
    }

    public boolean add(T elem) {
        // TODO
        return false;
    }

    public T remove(T value) {
        // TODO
        return null;
    }

    public void clear() {
        // TODO
    }

    public int size() {
        // TODO
        return 0;
    }

    private class Node {
        T value;
        Node left, right, parent;

        public Node(T v) {
            value = v;
        }

        public Node(T value, Node left, Node right, Node parent) {
            super();
            this.value = value;
            this.left = left;
            this.right = right;
            this.parent = parent;
        }
    }

}
