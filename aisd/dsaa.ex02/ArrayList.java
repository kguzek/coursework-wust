package dsaa.ex02;

import dsaa.util.AbstractList;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class ArrayList<E> extends AbstractList<E> {
    /**
     * <b> Domyślna</b> wielkość początkowa tablicy
     */
    private static final int DEFAULT_INITIAL_CAPACITY = 16;
    /**
     * <b> Początkowa</b> wielkość tablicy.
     */
    private final int _initialCapacity;
    /**
     * Referencja na tablicę zawierającą elementy
     */
    private E[] _array;
    /**
     * Rozmiar tablicy traktowanej jako lista
     */
    private int _size;

    @SuppressWarnings("unchecked")
    public ArrayList(int capacity) {
        if (capacity <= 0)
            capacity = DEFAULT_INITIAL_CAPACITY;
        _initialCapacity = capacity;
        _array = (E[]) (new Object[capacity]);
        _size = 0;
    }

    public ArrayList() {
        this(DEFAULT_INITIAL_CAPACITY);
    }

    @Override
    public boolean isEmpty() {
        return _size == 0;
    }

    @Override
    public int size() {
        return _size;
    }

    /**
     * Rozszerzenie tablicy, jeśli za mało miejsca w obecnej
     */
    @SuppressWarnings("unchecked")
    private void ensureCapacity(int capacity) {
        if (_array.length < capacity) {
            E[] copy = (E[]) (new Object[capacity + capacity / 2]);
            System.arraycopy(_array, 0, copy, 0, _size);
            _array = copy;
        }
    }

    // sprawdzenie poprawności indeksu
    private void checkOutOfBounds(int index) throws IndexOutOfBoundsException {
        if (index < 0 || index >= _size) throw new IndexOutOfBoundsException();
    }

    @SuppressWarnings("unchecked")
    @Override
    public void clear() {
        _array = (E[]) (new Object[_initialCapacity]);
        _size = 0;
    }

    @Override
    public boolean add(E value) {
        ensureCapacity(_size + 1);
        _array[_size] = value;
        _size++;
        return true;
    }

    @Override
    public void add(int index, E value) {
        if (index < 0 || index > _size) throw new IndexOutOfBoundsException();
        ensureCapacity(_size + 1);
        if (index != _size)
            System.arraycopy(_array, index, _array, index + 1, _size - index);
        _array[index] = value;
        _size++;
//        return false;
    }

    @Override
    public int indexOf(E value) {
        for (int i = 0; i < _size; i++) {
            if (value.equals(_array[i])) {
                return i;
            }
        }
        return -1;
    }

    @Override
    public boolean contains(E value) {
        return indexOf(value) != -1;
    }

    @Override
    public E get(int index) {
        checkOutOfBounds(index);
        return _array[index];
    }

    @Override
    public E set(int index, E element) {
        checkOutOfBounds(index);
        E retValue = _array[index];
        _array[index] = element;
        return retValue;
    }

    @Override
    public E remove(int index) {
        checkOutOfBounds(index);
        E retValue = _array[index];
        int copyFrom = index + 1;
        if (copyFrom < _size) System.arraycopy(_array, copyFrom, _array, index, _size - copyFrom);
        --_size;
        return retValue;
    }

    @Override
    public boolean remove(E value) {
        int pos = 0;
        while (pos < _size && !_array[pos].equals(value))
            pos++;
        if (pos < _size) {
            remove(pos);
            return true;
        }
        return false;
    }

    @Override
    public Iterator<E> iterator() {
        return new InnerIterator();
    }

    @Override
    public ListIterator<E> listIterator() {
        return new InnerListIterator();
    }

    private class InnerIterator implements Iterator<E> {
        int _pos = 0;

        @Override
        public boolean hasNext() {
            return _pos < _size;
        }

        @Override
        public E next() {
            return _array[_pos++];
        }
    }

    private class InnerListIterator implements ListIterator<E> {
        int _pos = 0;
        boolean _wasNext = false;
        boolean _wasPrevious = false;

        @Override
        public void add(E Value) {
            ArrayList.this.add(_pos, Value);
            _wasNext = false;
            _wasPrevious = false;
            _pos++;
        }

        @Override
        public boolean hasNext() {
            return _pos < _size;
        }

        @Override
        public boolean hasPrevious() {
            return _pos >= 0 && !isEmpty();
        }

        @Override
        public E next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            _wasNext = true;
            _wasPrevious = false;
            return _array[_pos++];
        }

        @Override
        public int nextIndex() {
            return _pos;
        }

        @Override
        public E previous() {
            if (!hasPrevious()) {
                throw new NoSuchElementException();
            }
            _wasPrevious = true;
            _wasNext = false;
            return _array[--_pos];
        }

        @Override
        public int previousIndex() {
            return _pos - 1;
        }

        /**
         * @return The index of the element last returned by {@link InnerListIterator#next()} or {@link InnerListIterator#previous()}.
         * @throws IllegalStateException if neither {@link InnerListIterator#next()} nor {@link InnerListIterator#previous()} was called.
         */
        private int getCurrentIndex() throws IllegalStateException {
            if (_wasNext) {
                return _pos - 1;
            }
            if (_wasPrevious) {
                return _pos;
            }
            throw new IllegalStateException("Neither next nor previous was called");
        }

        @Override
        public void remove() {
            ArrayList.this.remove(getCurrentIndex());
            if (_wasNext) {
                _pos--;
            }
            _wasPrevious = false;
            _wasNext = false;
        }

        @Override
        public void set(E e) {
            ArrayList.this.set(getCurrentIndex(), e);
        }
    }
}