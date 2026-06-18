package dsaa.list03.ex03;

import dsaa.util.EmptyQueueException;
import dsaa.util.IQueue;

import java.util.EmptyStackException;
import java.util.NoSuchElementException;
import java.util.Stack;

public class StackQueue<E> implements IQueue<E> {
    private final Stack<E> inbox = new Stack<>();
    private final Stack<E> outbox = new Stack<>();

    @Override
    public boolean isEmpty() {
        return inbox.isEmpty() && outbox.isEmpty();
    }

    @Override
    public boolean isFull() {
        return false;
    }

    @Override
    public E dequeue() throws EmptyQueueException {
        try {
            if (outbox.isEmpty()) {
                while (!inbox.isEmpty()) {
                    outbox.push(inbox.pop());
                }
            }
            return outbox.pop();
        } catch (NoSuchElementException | EmptyStackException e) {
            throw new EmptyQueueException();
        }
    }

    @Override
    public void enqueue(E elem) {
        inbox.push(elem);
    }

    @Override
    public int size() {
        return inbox.size() + outbox.size();
    }

    @Override
    public E first() {
        throw new UnsupportedOperationException();
    }
}
