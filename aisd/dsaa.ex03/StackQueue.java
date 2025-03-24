package dsaa.ex03;

import dsaa.util.EmptyQueueException;
import dsaa.util.IQueue;

import java.util.EmptyStackException;
import java.util.NoSuchElementException;
import java.util.Stack;

public class StackQueue<E> implements IQueue<E> {
    private final Stack<E> stack1 = new Stack<>();
    private final Stack<E> stack2 = new Stack<>();

    @Override
    public boolean isEmpty() {
        return stack1.isEmpty();
    }

    @Override
    public boolean isFull() {
        return false;
    }

    @Override
    public E dequeue() throws EmptyQueueException {
        try {
            stack1.removeFirst();
            return stack2.pop();
        } catch (NoSuchElementException | EmptyStackException e) {
            throw new EmptyQueueException();
        }
    }

    @Override
    public void enqueue(E elem) {
        stack1.push(elem);
        stack2.addFirst(elem);
    }

    @Override
    public int size() {
        return stack1.size();
    }

    @Override
    public E first() throws EmptyQueueException {
        try {
            return stack2.peek();
        } catch (EmptyStackException e) {
            throw new EmptyQueueException();
        }
    }
}
