package dsaa.ex03;

import dsaa.util.EmptyStackException;
import dsaa.util.FullStackException;

public class ReversibleArrayStack<E> extends ArrayStack<E> {
    public ReversibleArrayStack() {
        super();
    }

    public ReversibleArrayStack(int capacity) {
        super(capacity);
    }

    /**
     * Reverses all elements in the stack. Time complexity: O(3n)
     */
    public void reverse() {
        ArrayStack<E> tempStack1 = new ArrayStack<>(size());
        while (!isEmpty()) {
            try {
                tempStack1.push(pop());
            } catch (FullStackException | EmptyStackException e) {
                assert false : "Failed to copy elements from this stack to tempStack1.";
            }
        }
        ArrayStack<E> tempStack2 = new ArrayStack<>(tempStack1.size());
        while (!tempStack1.isEmpty()) {
            try {
                tempStack2.push(tempStack1.pop());
            } catch (FullStackException | EmptyStackException e) {
                assert false : "Failed to copy elements from tempStack1 to tempStack2.";
            }
        }
        while (!tempStack2.isEmpty()) {
            try {
                push(tempStack2.pop());
            } catch (FullStackException | EmptyStackException e) {
                assert false : "Failed to copy elements from tempStack2 to this stack.";
            }
        }
    }
}
