package dsaa.list03.ex02;


import dsaa.list03.ex01.ArrayStack;

public class ReversibleArrayStack<E> extends ArrayStack<E> implements IStackReversible<E> {
    public ReversibleArrayStack(int initialSize) {
        super(initialSize);
    }

    public ReversibleArrayStack() {
        super();
    }
}
