package dsaa.ex03;


public class ReversibleArrayStackReversible<E> extends ArrayStack<E> implements IStackReversible<E> {
    public ReversibleArrayStackReversible(int initialSize) {
        super(initialSize);
    }

    public ReversibleArrayStackReversible() {
        super();
    }
}
