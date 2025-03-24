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
     * Reverses all elements in the stack. Time complexity: O(2n)
     */
    public void reverse() {
        ArrayStack<E> tempStack = new ArrayStack<>(size());
        while (!isEmpty()) {
            try {
                tempStack.push(pop());
            } catch (FullStackException | EmptyStackException e) {
                assert false : "Failed to copy elements from this stack to tempStack.";
            }
        }
        while (!tempStack.isEmpty()) {
            try {
                push(tempStack.pop());
            } catch (FullStackException | EmptyStackException e) {
                assert false : "Failed to copy elements from tempStack to this stack.";
            }
        }
    }
}
