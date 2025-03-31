package dsaa.lab04;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class TwoWayCycledOrderedListWithSentinel<E extends Comparable<E>> implements IList<E> {

    private class Element {
        private final E object;
        private Element next = null;
        private Element prev = null;

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
            if (elem == this) {
                return;
            }
            elem.prev = this;
            elem.next = next;
            next.prev = elem;
            next = elem;
        }

        // assert it is NOT a sentinel
        public void remove() {
            prev.next = next;
            next.prev = prev;
        }
    }


    Element sentinel;
    private int size;

    private class InnerIterator implements Iterator<E> {
        private Element pos;

        public InnerIterator() {
            pos = sentinel;
        }

        @Override
        public boolean hasNext() {
            return pos.next != null && pos.next != sentinel;
        }

        @Override
        public E next() {
            pos = pos.next;
            return pos.object;
        }
    }

    @SuppressWarnings({"duplicates"})
    private class InnerListIterator implements ListIterator<E> {
        private int index = 0;
        private boolean wasNext = false;
        private boolean wasPrevious = false;
        private Element next;
        private Element prev;

        public InnerListIterator() {
            next = sentinel.next;
            prev = sentinel;
        }

        @Override
        public void add(E e) {
            Element newElement = new Element(e, prev, next);
            (prev == null ? sentinel : prev).addAfter(newElement);
            prev = newElement;
            index++;
        }

        @Override
        public boolean hasNext() {
            return next != null && next != sentinel;
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
            return prev != null && prev != sentinel;
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
                prev.remove();
            } else if (wasPrevious) {
                next.remove();
            } else {
                throw new IllegalStateException("remove must be called after next or previous");
            }
            size--;
        }

        @Override
        public void set(E e) {
            throw new UnsupportedOperationException();
        }
    }

    public TwoWayCycledOrderedListWithSentinel() {
        clear();
    }

    @Override
    public boolean add(E e) {
        Element newElement = new Element(e);
        Element current = sentinel;
        while (current.next != null && current.next != sentinel) {
            if (current.next.object.compareTo(e) > 0) {
                break;
            }
            current = current.next;
        }
        current.addAfter(newElement);
        size++;
        return true;
    }

    private void throwOnInvalidIndex(int index) {
        if (index < 0 || index >= size()) {
            throw new NoSuchElementException();
        }
    }

    @Override
    public void add(int index, E element) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void clear() {
        sentinel = new Element(null);
        sentinel.next = sentinel;
        sentinel.prev = sentinel;
        size = 0;
    }

    @Override
    public boolean contains(E element) {
        for (E elem : this) {
            if (elem.equals(element)) {
                return true;
            }
            if (element.compareTo(elem) < 0) {
                break;
            }
        }
        return false;
    }

    @Override
    public E get(int index) {
        throwOnInvalidIndex(index);
        Iterator<E> it = iterator();
        for (int i = 0; i < index; i++) {
            it.next();
        }
        return it.next();
    }

    @Override
    public E set(int index, E element) {
        throw new UnsupportedOperationException();
    }

    @Override
    public int indexOf(E element) {
        Iterator<E> it = iterator();
        for (int i = 0; it.hasNext(); i++) {
            E current = it.next();
            if (current.equals(element)) {
                return i;
            }
            if (current.compareTo(element) < 0) {
                break;
            }
        }
        return -1;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
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
        throwOnInvalidIndex(index);
        ListIterator<E> it = listIterator();
        for (int i = 1; i < index; i++) {
            it.next();
        }
        E result = it.next();
        it.remove();
        return result;
    }

    @Override
    public boolean remove(E e) {
        ListIterator<E> it = listIterator();
        while (it.hasNext()) {
            E current = it.next();
            if (current.equals(e)) {
                it.remove();
                return true;
            }
            if (current.compareTo(e) > 0) {
                break;
            }
        }
        return false;
    }

    @Override
    public int size() {
        return size;
    }

    //@SuppressWarnings("unchecked")
    public void add(TwoWayCycledOrderedListWithSentinel<E> other) {
        if (this == other || other.isEmpty()) {
            return;
        }
        if (isEmpty()) {
            sentinel = other.sentinel;
            other.clear();
            return;
        }
        Element thisCurrent = sentinel;
        for (Element otherCurrent = other.sentinel.next; otherCurrent != null && otherCurrent != other.sentinel; ) {
            while (thisCurrent.next != null && thisCurrent.next != sentinel) {
                if (thisCurrent.next.object.compareTo(otherCurrent.object) > 0) {
                    break;
                }
                thisCurrent = thisCurrent.next;
            }
            Element otherNext = otherCurrent.next;
            thisCurrent.addAfter(otherCurrent);
            otherCurrent = otherNext;
        }
        size += other.size;
        other.clear();
    }

    //@SuppressWarnings({ "unchecked", "rawtypes" })
    public void removeAll(E e) {
        ListIterator<E> it = listIterator();
        while (it.hasNext()) {
            E current = it.next();
            if (e.equals(current)) {
                it.remove();
            } else if (current.compareTo(e) > 0) {
                return;
            }
        }
    }
}

