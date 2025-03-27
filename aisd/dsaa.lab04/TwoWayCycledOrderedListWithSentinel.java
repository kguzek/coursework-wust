package dsaa.lab04;

import java.util.Iterator;
import java.util.ListIterator;

public class TwoWayCycledOrderedListWithSentinel<E> implements IList<E> {

    private class Element {
        public Element(E e) {
            this.object = e;
        }

        public Element(E e, Element next, Element prev) {
            this.object = e;
            this.next = next;
            this.prev = prev;
        }

        // add element e after this
        public void addAfter(Element elem) {
            if (next != null) {
                elem.next = next;
            }
            elem.prev = this;
            elem.next = null;
            next = elem;
        }

        // assert it is NOT a sentinel
        public void remove() {
            if (object != null) {
                prev.next = next;
                next.prev = prev;
            }
        }

        E object;
        Element next = null;
        Element prev = null;
    }


    Element sentinel;
    int size;

    private class InnerIterator implements Iterator<E> {
        private Element pos;

        public InnerIterator() {
            pos = new Element(null, sentinel, null);
        }

        @Override
        public boolean hasNext() {
            return pos != null && pos.next != null;
        }

        @Override
        public E next() {
            pos = pos.next;
            return pos.object;
        }
    }

    private class InnerListIterator implements ListIterator<E> {
        //TODO
        public InnerListIterator() {
            //TODO
        }

        @Override
        public boolean hasNext() {
            //TODO
            return false;
        }

        @Override
        public E next() {
            //TODO
            return null;
        }

        @Override
        public void add(E arg0) {
            throw new UnsupportedOperationException();
        }

        @Override
        public boolean hasPrevious() {
            //TODO
            return false;
        }

        @Override
        public int nextIndex() {
            throw new UnsupportedOperationException();
        }

        @Override
        public E previous() {
            //TODO
            return null;
        }

        @Override
        public int previousIndex() {
            throw new UnsupportedOperationException();
        }

        @Override
        public void remove() {
            throw new UnsupportedOperationException();
        }

        @Override
        public void set(E arg0) {
            throw new UnsupportedOperationException();
        }
    }

    public TwoWayCycledOrderedListWithSentinel() {
        //TODO
    }

    //@SuppressWarnings("unchecked")
    @Override
    public boolean add(E e) {
        //TODO
        return false;
    }

    private Element getElement(int index) {
        //TODO
        return null;
    }

    private Element getElement(E obj) {
        //TODO
        return null;
    }

    @Override
    public void add(int index, E element) {
        throw new UnsupportedOperationException();

    }

    @Override
    public void clear() {
        //TODO
    }

    @Override
    public boolean contains(E element) {
        //TODO
        return false;
    }

    @Override
    public E get(int index) {
        //TODO
        return null;
    }

    @Override
    public E set(int index, E element) {
        throw new UnsupportedOperationException();
    }

    @Override
    public int indexOf(E element) {
        //TODO
        return -1;
    }

    @Override
    public boolean isEmpty() {
        //TODO
        return true;
    }

    @Override
    public Iterator<E> iterator() {
        return new InnerIterator();
    }

    @Override
    public ListIterator<E> listIterator() {
        return new InnerListIterator();
    }

    @Override
    public E remove(int index) {
        //TODO
        return null;
    }

    @Override
    public boolean remove(E e) {
        //TODO
        return false;
    }

    @Override
    public int size() {
        //TODO
        return -1;
    }

    //@SuppressWarnings("unchecked")
    public void add(TwoWayCycledOrderedListWithSentinel<E> other) {
        //TODO
    }

    //@SuppressWarnings({ "unchecked", "rawtypes" })
    public void removeAll(E e) {
        //TODO
    }

}

