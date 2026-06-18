package dsaa.list03.ex02;

import dsaa.list02.ex02.OneWayLinkedListWithHead;
import dsaa.util.EmptyStackException;
import dsaa.util.IList;
import dsaa.util.IStack;

public class ListStack<E> implements IStack<E> {
    IList<E> _list;

    public ListStack() {
        _list = new OneWayLinkedListWithHead<>();
    }

    @Override
    public boolean isEmpty() {
        return _list.isEmpty();
    }

    @Override
    public boolean isFull() {
        return false;
    }

    @Override
    public E pop() throws EmptyStackException {
        E value = _list.remove(0);
        if (value == null) throw new EmptyStackException();
        return value;
    }

    @Override
    public void push(E elem) {
        _list.add(0, elem);
    }

    @Override
    public int size() {
        return _list.size();
    }

    @Override
    public E top() throws EmptyStackException {
        E value = _list.get(0);
        if (value == null) throw new EmptyStackException();
        return value;
    }
}
