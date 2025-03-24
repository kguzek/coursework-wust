package dsaa.ex03;


public class ReversibleArrayStack<E> extends ArrayStack<E> implements IStackReversible<E> {
    public ReversibleArrayStack(int initialSize) {
        super(initialSize);
    }

    public ReversibleArrayStack() {
        super();
    }
}
