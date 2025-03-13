package dsaa.lab02;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class OneWayLinkedList<E> implements IList<E> {

    private class Element {
        public Element(E e) {
            object = e;
        }

        E object;
        Element next = null;
    }

    Element sentinel;

    private class InnerIterator implements Iterator<E> {
        Element current;

        public InnerIterator() {
            current = sentinel;
        }

        @Override
        public boolean hasNext() {
            return current != null && current.next != null;
        }

        @Override
        public E next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            current = current.next;
            return current.object;
        }
    }

    public OneWayLinkedList() {
        sentinel = new Element(null);
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
    public boolean add(E e) {
        Element last = sentinel;
        while (last.next != null) {
            last = last.next;
        }
        last.next = new Element(e);
        return true;
    }

    /**
     * Gets the element handle at index, throwing NoSuchElementException if it doesn't exist or if it has no child
     */
    private Element getParentAt(int index) throws NoSuchElementException {
        Element parent = sentinel;
        if (index == 0) {
            throw new NoSuchElementException();
        }
        for (int i = 0; i < index; i++) {
            if (parent.next == null || parent.next.next == null) {
                throw new NoSuchElementException();
            }
            parent = parent.next;
        }
        return parent;
    }

    @Override
    public void add(int index, E element) throws NoSuchElementException {
        Element parent = getParentAt(index);
        Element child = parent.next;
        Element newChild = new Element(element);
        newChild.next = child;
        parent.next = newChild;
    }

    @Override
    public void clear() {
        sentinel.next = null;
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
    public E get(int index) throws NoSuchElementException {
        Iterator<E> it = iterator();
        E element = null;
        for (int i = 0; i <= index; i++) {
            element = it.next();
        }
        return element;
    }

    @Override
    public E set(int index, E element) throws NoSuchElementException {
        Element child = sentinel;
        for (int i = 0; i <= index; i++) {
            if (child.next == null) {
                throw new NoSuchElementException();
            }
            child = child.next;
        }
        child.object = element;
        return element;
    }

    @Override
    public int indexOf(E element) {
        for (int i = 0; i < size(); i++) {
            if (get(i).equals(element)) {
                return i;
            }
        }
        return 0;
    }

    @Override
    public boolean isEmpty() {
        return sentinel.next == null;
    }

    @Override
    public E remove(int index) throws NoSuchElementException {
        Element parent = getParentAt(index);
        Element child = parent.next;
        parent.next = child.next;
        return child.object;
    }

    @Override
    public boolean remove(E e) {
        try {
            remove(indexOf(e));
        } catch (NoSuchElementException _ex) {
            return false;
        }
        return true;
    }

    @Override
    public int size() {
        int size = 0;
        for (E _e : this) {
            size++;
        }
        return size;
    }

}

