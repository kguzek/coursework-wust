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
    private int size;

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
        size = 0;
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
        size++;
        return true;
    }

    /**
     * Gets the element handle at index, throwing NoSuchElementException if it doesn't exist or if it has no child
     */
    private Element getParentAt(int index) throws NoSuchElementException {
        Element parent = sentinel;
        for (int i = 0; i < index; i++) {
            if (parent.next == null) {
                throw new NoSuchElementException();
            }
            parent = parent.next;
        }
//        if (parent.next == null) {
//            throw new NoSuchElementException();
//        }
        return parent;
    }

    @Override
    public void add(int index, E element) throws NoSuchElementException {
        Element parent = getParentAt(index);
        Element child = parent.next;
        Element newChild = new Element(element);
        newChild.next = child;
        parent.next = newChild;
        size++;
    }

    @Override
    public void clear() {
        sentinel.next = null;
        size = 0;
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
        E oldValue = child.object;
        child.object = element;
        return oldValue;
    }

    @Override
    public int indexOf(E element) {
        Element current = sentinel.next;
        for (int i = 0; current != null; i++) {
            if (element.equals(current.object)) {
                return i;
            }
            current = current.next;
        }
        return -1;
    }

    @Override
    public boolean isEmpty() {
        return sentinel.next == null;
    }

    @Override
    public E remove(int index) throws NoSuchElementException {
        Element parent = getParentAt(index);
        Element child = parent.next;
        if (child == null) {
            throw new NoSuchElementException();
        }
        parent.next = child.next;
        size--;
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
        return size;
    }

}

