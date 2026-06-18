package dsaa.list07.ex01;

import dsaa.list07.BinarySearchTree;
import dsaa.list07.DuplicateElementException;

public class InsertSequenceBST {
    private static final BinarySearchTree<Integer> tree = new BinarySearchTree<>(Integer::compareTo);

    public static void main(String[] args) throws DuplicateElementException {
        tree.insert(20);
        tree.insert(7);
        tree.insert(10);
        tree.insert(25);
        tree.insert(4);
        tree.insert(1);
        tree.insert(2);
        tree.insert(12);
        tree.insert(30);
        tree.delete(12);
        tree.delete(1);
        tree.delete(20);
        System.out.println(tree);
    }
}
