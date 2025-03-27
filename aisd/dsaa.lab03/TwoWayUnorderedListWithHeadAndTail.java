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

    private Element head;
    private Element tail;
    private int _size;

    private class InnerIterator implements Iterator<E> {
        private Element pos;

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

    private class InnerListIterator implements ListIterator<E> {
        private int index = 0;
        private boolean wasNext = false;
        private boolean wasPrevious = false;
        private Element next;
        private Element prev;

        public InnerListIterator() {
            super();
            next = head;
            prev = null;
        }

        @Override
        public void add(E e) {
            Element newElement = new Element(e);
            if (hasPrevious()) {
                newElement.prev = prev;
                prev.next = newElement;
            } else {
                head = newElement;
            }
            if (hasNext()) {
                newElement.next = next;
                next.prev = newElement;
            } else {
                tail = newElement;
            }
            prev = newElement;
            index++;
        }

        @Override
        public boolean hasNext() {
            return next != null;
        }

        @Override
        public E next() {
            Element current = next;
            next = next.next;
            prev = current;
            index++;
            wasNext = true;
            wasPrevious = false;
            return current.object;
        }

        @Override
        public int nextIndex() {
            return hasNext() ? index + 1 : index;
        }

        @Override
        public boolean hasPrevious() {
            return prev != null;
        }

        @Override
        public E previous() {
            Element current = prev;
            prev = prev.prev;
            next = current;
            index--;
            wasPrevious = true;
            wasNext = false;
            return current.object;
        }

        @Override
        public int previousIndex() {
            return hasPrevious() ? index - 1 : -1;
        }

        @Override
        public void remove() {
            if (wasNext) {
                if (hasPrevious() && prev.prev != null) {
                    prev.prev.next = next;
                    prev = prev.prev;
                } else {
                    head = next;
                    if (hasNext()) {
                        next.prev = null;
                    }
                }
                if (hasNext()) {
                    next.prev = prev;
                } else {
                    tail = prev;
                    if (hasPrevious()) {
                        prev.next = null;
                    }
                }
            } else if (wasPrevious) {
                if (hasNext()) {
                    next.prev = prev;
                }
                if (hasPrevious()) {
                    prev.next = next;
                } else {
                    head = next;
                    if (hasNext()) {
                        next.prev = null;
                    }
                }
            } else {
                throw new IllegalStateException();
            }
        }

        @Override
        public void set(E e) {
            if (wasNext) {
                prev.object = e;
            } else if (wasPrevious) {
                next.object = e;
            } else {
                throw new IllegalStateException();
            }
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
    public void add(int index, E element) {
        if (index < 0 || index > size()) {
            throw new NoSuchElementException();
        }
        if (index == size()) {
            add(element);
            return;
        }
        ListIterator<E> it = listIterator();
        for (int i = 0; i < index; i++) {
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

    private void throwIfIndexOutOfBounds(int index) {
        if (index < 0 || index >= size()) {
            throw new NoSuchElementException();
        }
    }

    @Override
    public E get(int index) {
        throwIfIndexOutOfBounds(index);
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
        throwIfIndexOutOfBounds(index);
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
        throwIfIndexOutOfBounds(index);
        ListIterator<E> it = listIterator();
        for (int i = 0; i < index; i++) {
            it.next();
        }
        E removedElement = it.next();
        if (size() == 1) {
            clear();
        } else {
            it.remove();
            _size--;
        }
        return removedElement;
    }

    @Override
    public boolean remove(E e) {
        if (size() == 1) {
            clear();
            return true;
        }
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
        ListIterator<E> iter = listIterator();
        while (iter.hasNext()) {
            iter.next();
        }
        StringBuilder bob = new StringBuilder();
        while (iter.hasPrevious()) {
            bob.append("\n").append(iter.previous());
        }
        return bob.toString();
    }

    public void add(TwoWayUnorderedListWithHeadAndTail<E> other) {
        if (other == this || other.isEmpty()) {
            return;
        }
        if (isEmpty()) {
            head = other.head;
            tail = other.tail;
            _size = other.size();
            other.clear();
            return;
        }
        tail.next = other.head;
        other.head.prev = tail;
        tail = other.tail;
        _size += other.size();
        other.clear();
    }

    public void removeDuplicates() {
        if (size() <= 1) {
            return;
        }
        ListIterator<E> it = listIterator();
        E previous = it.next();
        while (it.hasNext()) {
            E current = it.next();
            if (current.equals(previous)) {
                it.remove();
            } else {
                previous = current;
            }
        }
    }
}

