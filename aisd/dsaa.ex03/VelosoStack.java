package dsaa.ex03;

import dsaa.util.EmptyStackException;
import dsaa.util.FullStackException;
import dsaa.util.IStack;

public class VelosoStack<E> extends ArrayStack<E> implements IStack<E> {
    private int position = -1;

    public VelosoStack(int size) {
        super(size);
    }

    E peek() {
        if (position < 0) {
            throw new IndexOutOfBoundsException();
        }
        return array[position];
    }

    @Override
    public E top() throws EmptyStackException {
        position = topIndex - 1;
        // TODO: not null?
        return null;
    }

    @Override
    public void push(E elem) throws FullStackException {
        super.push(elem);
        try {
            top();
        } catch (EmptyStackException e) {
            assert false : "Stack is empty after pushing";
        }
    }

    @Override
    public E pop() throws EmptyStackException {
        E popped = super.pop();
        top();
        return popped;
    }

    void down() {
        if (position == 0) {
            throw new IndexOutOfBoundsException();
        }
        position--;
    }
}
