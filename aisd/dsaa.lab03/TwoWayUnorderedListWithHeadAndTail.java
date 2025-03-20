package dsaa.lab03;

import java.util.Iterator;
import java.util.ListIterator;


public class TwoWayUnorderedListWithHeadAndTail<E> implements IList<E> {

    private class Element {
        public Element(E e) {
            this.object = e;
        }

        public Element(E e, Element next, Element prev) {
            this.object = e;
            this.prev = prev;
            this.next = next;
        }

        E object;
        Element next = null;
        Element prev = null;
    }

    Element head;
    Element tail;
    // can be realization with the field size or without
    int _size;

    private class InnerIterator implements Iterator<E> {
        Element pos;

        public InnerIterator() {
            pos = head;
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

    private class InnerListIterator extends InnerIterator implements ListIterator<E> {
        boolean removed = false;
        boolean added = false;
        int index = 0;
        boolean wasNext = false;
        boolean wasPrevious = false;

        @Override
        public void add(E e) {
            Element newElement = new Element(e);
            if (pos == null) {
                pos = newElement;
            } else {
                if (hasNext()) {
                    pos.next.prev = newElement;
                    newElement.next = pos.next;
                }
                pos.next = newElement;
            }
            next();
            added = true;
        }

        @Override
        public E next() {
            E element = super.next();
            index++;
            wasNext = true;
            added = false;
            removed = false;
            return element;
        }

        @Override
        public int nextIndex() {
            return hasNext() ? index + 1 : index;
        }

        @Override
        public boolean hasPrevious() {
            return pos != null && pos.prev != null;
        }

        @Override
        public E previous() {
            pos = pos.prev;
            index--;
            wasPrevious = true;
            added = false;
            removed = false;
            return pos.object;
        }

        @Override
        public int previousIndex() {
            return hasPrevious() ? index - 1 : -1;
        }

        @Override
        public void remove() {
            try {
                if (wasNext) {
                    pos.prev.next = pos.next;
                    pos.next.prev = pos.prev;
                } else if (wasPrevious) {
                    pos.next.prev = pos.prev;
                    pos.prev.next = pos.next;
                } else {
                    throw new IllegalStateException();
                }
            } catch (NullPointerException e) {
                throw new IllegalStateException(e);
            }
            removed = true;
        }

        @Override
        public void set(E e) {
            pos.object = e;
        }
    }

    public TwoWayUnorderedListWithHeadAndTail() {
        // make a head and a tail
        head = null;
        tail = null;
        _size = 0;
    }

    @Override
    public boolean add(E e) {
        Element newElement = new Element(e, null, tail);
        if (isEmpty()) {
            head = newElement;
            tail = newElement;
        } else {
            tail.next = newElement;
        }
        _size++;
        return true;
    }

    @Override
    public void add(int index, E element) {
        //TODO
    }

    @Override
    public void clear() {
        head = null;
        tail = null;
        _size = 0;
    }

    @Override
    public boolean contains(E element) {
        for (E elem : this) {
            if (elem.equals(element)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public E get(int index) {
        Iterator<E> it = iterator();
        for (int i = 0; it.hasNext(); i++) {
            E element = it.next();
            if (i == index) {
                return element;
            }
        }
        return null;
    }

    @Override
    public E set(int index, E element) {
        ListIterator<E> it = listIterator();
        for (int i = 0; i < index; i++) {
            it.next();
        }
        E oldElement = it.next();
        it.set(element);
        return oldElement;
    }

    @Override
    public int indexOf(E element) {
        Iterator<E> it = iterator();
        for (int i = 0; it.hasNext(); i++) {
            if (it.next().equals(element)) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public boolean isEmpty() {
        return head == null || tail == null;
    }

    @Override
    public Iterator<E> iterator() {
        return new InnerIterator();
    }

    @Override
    public ListIterator<E> listIterator() {
        throw new UnsupportedOperationException();
    }

    @Override
    public E remove(int index) {
        //TODO
        return null;
    }

    @Override
    public boolean remove(E e) {
        //TODO
        return true;
    }

    @Override
    public int size() {
        return _size;
    }

    public String toStringReverse() {
        ListIterator<E> iter = new InnerListIterator();
        while (iter.hasNext())
            iter.next();
        String retStr = "";
        //TODO use reverse direction of the iterator
        return retStr;
    }

    public void add(TwoWayUnorderedListWithHeadAndTail<E> other) {
        //TODO
    }
}

