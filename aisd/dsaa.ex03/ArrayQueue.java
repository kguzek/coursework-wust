package dsaa.ex03;

import dsaa.util.EmptyQueueException;
import dsaa.util.FullQueueException;
import dsaa.util.IQueue;

public class ArrayQueue<T> implements IQueue<T> {
    private static final int DEFAULT_CAPACITY = 16;
    T[] array;
    int beginIndex;
    int endIndex;

    @SuppressWarnings("unchecked")
    public ArrayQueue(int size) {
        array = (T[]) new Object[size + 1];
    }

    public ArrayQueue() {
        this(DEFAULT_CAPACITY);
    }

    @Override
    public boolean isEmpty() {
        return beginIndex == endIndex;
    }

    @Override
    public boolean isFull() {
        return beginIndex == (endIndex + 1) % array.length;
    }

    @Override
    public T dequeue() throws EmptyQueueException {
        if (isEmpty())
            throw new EmptyQueueException();
        T retValue = array[beginIndex++];
        beginIndex %= array.length;
        return retValue;
    }

    @Override
    public void enqueue(T elem) throws FullQueueException {
        if (isFull())
            throw new FullQueueException();
        array[endIndex++] = elem;
        endIndex %= array.length;
    }

    @Override
    public int size() {
        return (endIndex + array.length - beginIndex) % array.length;
    }

    @Override
    public T first() throws EmptyQueueException {
        if (isEmpty())
            throw new EmptyQueueException();
        return array[beginIndex];
    }
}
