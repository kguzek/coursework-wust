package dsaa.ex03;

import dsaa.util.EmptyStackException;
import dsaa.util.FullStackException;
import dsaa.util.IStack;

public interface IStackReversible<E> extends IStack<E> {
    /**
     * Reverses all elements in the stack using temporary instances of {@link ListStack}. Time complexity: O(3n)
     */
    default void reverse() {
        IStack<E> tempStack1 = new ListStack<>();
        while (!isEmpty()) {
            try {
                tempStack1.push(pop());
            } catch (FullStackException | EmptyStackException e) {
                assert false : "Failed to copy elements from this stack to tempStack1.";
            }
        }
        IStack<E> tempStack2 = new ListStack<>();
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
