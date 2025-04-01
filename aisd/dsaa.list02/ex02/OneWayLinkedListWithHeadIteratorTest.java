package dsaa.list02.ex02;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Iterator;

import static dsaa.util.Common.listToArray;
import static org.junit.jupiter.api.Assertions.*;

public class OneWayLinkedListWithHeadIteratorTest {
    private OneWayLinkedListWithHead<String> list;

    @BeforeEach
    public void setUp() {
        list = new OneWayLinkedListWithHead<>();
        list.add("A");
        list.add("B");
        list.add("C");
    }

    @Test
    public void testRemoveOnlyElement() {
        OneWayLinkedListWithHead<String> singleElementList = new OneWayLinkedListWithHead<>();
        singleElementList.add("X");
        Iterator<String> it = singleElementList.iterator();

        it.next();
        it.remove();

        assertEquals(0, singleElementList.size());
        assertFalse(singleElementList.iterator().hasNext());
    }

    @Test
    public void testRemoveHead() {
        Iterator<String> it = list.iterator();
        it.next();
        it.remove();

        assertEquals(2, list.size());
        assertEquals("B", list.iterator().next());
        assertArrayEquals(new String[]{"B", "C"}, listToArray(list));
    }

    @Test
    public void testRemoveMiddle() {
        Iterator<String> it = list.iterator();
        it.next(); // A
        it.next(); // B
        it.remove();

        assertEquals(2, list.size());
        assertArrayEquals(new String[]{"A", "C"}, listToArray(list));

        // Verify iterator position after removal
        assertEquals("C", it.next());
    }

    @Test
    public void testRemoveLast() {
        Iterator<String> it = list.iterator();
        it.next(); // A
        it.next(); // B
        it.next(); // C
        it.remove();

        assertEquals(2, list.size());
        assertArrayEquals(new String[]{"A", "B"}, listToArray(list));
        assertFalse(it.hasNext());
    }

    @Test
    public void testRemoveWithoutNextThrowsException() {
        Iterator<String> it = list.iterator();
        IllegalStateException exception = assertThrows(IllegalStateException.class, it::remove);
        assertEquals("next() was not called", exception.getMessage());
    }

    @Test
    public void testConsecutiveRemovals() {
        Iterator<String> it = list.iterator();
        it.next(); // A
        it.remove();
        it.next(); // B
        it.remove();
        it.next(); // C
        it.remove();

        assertEquals(0, list.size());
        assertFalse(it.hasNext());
    }

    @Test
    public void testDoubleRemoveThrowsException() {
        Iterator<String> it = list.iterator();
        it.next();
        it.remove();
        IllegalStateException exception = assertThrows(IllegalStateException.class, it::remove);
        assertEquals("next() was not called", exception.getMessage());
    }

    @Test
    public void testSizeAfterRemovals() {
        Iterator<String> it = list.iterator();
        it.next();
        it.remove();
        assertEquals(2, list.size());

        it.next();
        it.remove();
        assertEquals(1, list.size());
    }

    @Test
    public void testIteratorAfterHeadRemoval() {
        Iterator<String> it = list.iterator();
        it.next();
        it.remove();
        it = list.iterator();
        assertEquals("B", it.next());
        assertEquals("C", it.next());
    }
}
