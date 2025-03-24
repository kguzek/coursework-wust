package dsaa.ex02;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ListIterator;
import java.util.NoSuchElementException;

import static dsaa.util.Common.listToArray;
import static org.junit.jupiter.api.Assertions.*;

public class ArrayListListIteratorTest {

    private ArrayList<String> list;
    private ListIterator<String> iterator;

    @BeforeEach
    void setUp() {
        list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add("C");
        iterator = list.listIterator();
    }

    // Core iterator navigation tests
    @Test
    void testNextNavigation() {
        assertTrue(iterator.hasNext());
        assertEquals("A", iterator.next());
        assertEquals(1, iterator.nextIndex());
        assertEquals("B", iterator.next());
    }

    @Test
    void testPreviousNavigation() {
        iterator.next();
        iterator.next(); // Move to position 2
        assertTrue(iterator.hasPrevious());
        assertEquals("B", iterator.previous());
        assertEquals(0, iterator.previousIndex());
    }

    // Modification operation tests
    @Test
    void testAddOperation() {
        iterator.next(); // Position 1
        iterator.add("X");
        assertEquals(4, list.size());
        assertEquals("X", list.get(1));
        assertEquals("B", iterator.next());
    }

    @Test
    void testSetOperation() {
        iterator.next();
        iterator.set("X");
        assertEquals("X", list.get(0));
    }

    // Exception handling tests
    @Test
    void testRemoveWithoutPreparation() {
        assertThrows(IllegalStateException.class, () -> iterator.remove());
    }

    @Test
    void testDoubleRemove() {
        iterator.next();
        iterator.remove();
        assertThrows(IllegalStateException.class, () -> iterator.remove());
    }

    // Edge case tests
    @Test
    void testEmptyListBehavior() {
        ArrayList<String> empty = new ArrayList<>();
        ListIterator<String> it = empty.listIterator();
        assertFalse(it.hasNext());
        assertFalse(it.hasPrevious());
        assertThrows(NoSuchElementException.class, it::next);
    }


    @Test
    void testSingleElementList() {
        ArrayList<String> single = new ArrayList<>();
        single.add("X");
        ListIterator<String> it = single.listIterator();
        assertTrue(it.hasNext());
        assertEquals("X", it.next());
        assertTrue(it.hasPrevious());
    }

    // ADD OPERATION TESTS
    @Test
    void testAddAtBeginning() {
        iterator.add("X"); // Add before first element
        assertArrayEquals(new String[]{"X", "A", "B", "C"}, listToArray(list));
        assertEquals(1, iterator.nextIndex()); // Cursor after added element
    }

    @Test
    void testAddInMiddleAfterNext() {
        iterator.next(); // Position 1 (after A)
        iterator.add("X");
        assertArrayEquals(new String[]{"A", "X", "B", "C"}, listToArray(list));
        assertEquals(2, iterator.nextIndex());
    }

    @Test
    void testAddAtEnd() {
        while (iterator.hasNext()) iterator.next(); // Reach end
        iterator.add("X");
        assertArrayEquals(new String[]{"A", "B", "C", "X"}, listToArray(list));
        assertEquals(4, iterator.nextIndex());
    }

    @Test
    void testAddToEmptyList() {
        list.clear();
        iterator = list.listIterator();
        iterator.add("X");
        assertArrayEquals(new String[]{"X"}, listToArray(list));
        assertFalse(iterator.hasNext());
    }

    // SET OPERATION TESTS
    @Test
    void testSetAfterNext() {
        iterator.next(); // A
        iterator.set("X");
        assertArrayEquals(new String[]{"X", "B", "C"}, listToArray(list));
    }

    @Test
    void testSetAfterPrevious() {
        iterator.next();
        iterator.next(); // B
        iterator.previous(); // Back to A-B boundary
        iterator.set("X");
        assertArrayEquals(new String[]{"A", "X", "C"}, listToArray(list));
    }

    @Test
    void testMultipleSets() {
        iterator.next(); // A
        iterator.set("X");
        iterator.next(); // B
        iterator.set("Y");
        assertArrayEquals(new String[]{"X", "Y", "C"}, listToArray(list));
    }

    // REMOVE OPERATION TESTS
    @Test
    void testRemoveAfterNext() {
        iterator.next(); // A
        iterator.remove();
        assertEquals(2, list.size());
        assertEquals("B", list.get(0));
        assertArrayEquals(new String[]{"B", "C"}, listToArray(list));
        assertEquals(0, iterator.nextIndex());
    }

    @Test
    void testRemoveAfterPrevious() {
        iterator.next();
        iterator.next(); // B
        iterator.previous(); // Back to A-B boundary
        iterator.remove(); // Remove B
        assertEquals(2, list.size());
        assertEquals("C", list.get(1));
        assertArrayEquals(new String[]{"A", "C"}, listToArray(list));
        assertEquals(1, iterator.nextIndex());
    }

    @Test
    void testRemoveOnlyElement() {
        list.clear();
        list.add("X");
        iterator = list.listIterator();
        iterator.next();
        iterator.remove();
        assertTrue(list.isEmpty());
        assertFalse(iterator.hasPrevious());
    }

    // COMBINATION OPERATION TESTS
    @Test
    void testAddThenRemove() {
        iterator.add("X");
        assertEquals(4, list.size());
        assertThrows(IllegalStateException.class, () -> iterator.remove());
        assertEquals("A", iterator.next());
        iterator.remove();
        assertArrayEquals(new String[]{"X", "B", "C"}, listToArray(list));
    }

    @Test
    void testRemoveThenAdd() {
        iterator.next(); // A
        iterator.remove();
        iterator.add("X");
        assertArrayEquals(new String[]{"X", "B", "C"}, listToArray(list));
        assertEquals(1, iterator.nextIndex());
    }

    // EXCEPTION CASES
    @Test
    void testSetWithoutPreparation() {
        assertThrows(IllegalStateException.class, () -> iterator.set("X"));
        iterator.add("Y");
        assertThrows(IllegalStateException.class, () -> iterator.set("Z"));
    }

    @Test
    void testRemoveAfterAdd() {
        iterator.add("X");
        assertThrows(IllegalStateException.class, () -> iterator.remove());
    }

    @Test
    void testConsecutiveRemoveCalls() {
        iterator.next();
        iterator.remove();
        assertThrows(IllegalStateException.class, () -> iterator.remove());
    }

    // INDEX VALIDATION
    @Test
    void testIndicesAfterAdd() {
        iterator.next(); // Position 1
        iterator.add("X");
        assertEquals(1, iterator.previousIndex());
        assertEquals(2, iterator.nextIndex());
    }

    @Test
    void testIndicesAfterRemove() {
        iterator.next(); // A
        iterator.next(); // B
        iterator.remove();
        assertEquals(1, iterator.nextIndex());
        assertEquals(0, iterator.previousIndex());
    }
}
