package dsaa.lab03;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;


public class TwoWayUnorderedListWithHeadAndTail<E> implements IList<E> {

    private class Element {
        public Element(E e) {
            this.object = e;
        }

        public Element(E e, Element next, Element prev) {
            this.object = e;
            this.next = next;
            this.prev = prev;
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
            pos = new Element(null, head, null);
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
                    if (hasNext()) {
                        pos.next.prev = pos.prev;
                    }
                } else if (wasPrevious) {
                    pos.next.prev = pos.prev;
                    if (hasPrevious()) {
                        pos.prev.next = pos.next;
                    }
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
        if (isEmpty()) {
            head = new Element(e);
            tail = head;
        } else if (size() == 1) {
            tail = new Element(e, null, head);
            head.next = tail;
        } else {
            tail.next = new Element(e, null, tail);
            tail = tail.next;
        }
        _size++;
        return true;
    }

    @Override
    public void add(int index, E element) throws NoSuchElementException {
        if (index < 0 || index > size()) {
            throw new NoSuchElementException();
        }
        if (index == size()) {
            add(element);
            return;
        }
        ListIterator<E> it = listIterator();
        for (int i = 0; i <= index; i++) {
            it.next();
        }
        it.add(element);
        _size++;
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
        return _size == 0;
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
        if (index < 0 || index >= size()) {
            throw new NoSuchElementException();
        }
        ListIterator<E> it = listIterator();
        for (int i = 0; i < index; i++) {
            it.next();
        }
        E removedElement = it.next();
        it.remove();
        _size--;
        return removedElement;
    }

    @Override
    public boolean remove(E e) {
        ListIterator<E> it = listIterator();
        while (it.hasNext()) {
            if (it.next().equals(e)) {
                it.remove();
                _size--;
                return true;
            }
        }
        return false;
    }

    @Override
    public int size() {
        return _size;
    }

    public String toStringReverse() {
        if (isEmpty()) {
            return "";
        }
        ListIterator<E> iter = listIterator();
        while (iter.hasNext() && iter.nextIndex() < size())
            iter.next();
        StringBuilder bob = new StringBuilder();
        bob.append("\n").append(iter.next());
        while (iter.hasPrevious()) {
            bob.append("\n");
            bob.append(iter.previous());
        }
        return bob.toString();
    }

    public void add(TwoWayUnorderedListWithHeadAndTail<E> other) {
        if (isEmpty()) {
            head = other.head;
            tail = other.tail;
            _size = other.size();
            other.clear();
            return;
        }
        if (other.isEmpty()) {
            return;
        }
        if (other == this) {
//            this will cause an OutOfMemoryError
            throw new UnsupportedOperationException();
        }
        tail.next = other.head;
        other.head.prev = tail;
        tail = other.tail;
        _size += other.size();
        other.clear();
    }
}

