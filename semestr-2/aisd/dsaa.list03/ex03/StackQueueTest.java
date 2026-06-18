package dsaa.list03.ex03;


import dsaa.util.EmptyQueueException;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class StackQueueTest {

    private StackQueue<Integer> queue;

    @Test
    void testIsEmpty() {
        queue = new StackQueue<>();
        assertTrue(queue.isEmpty());
    }

    @Test
    void testEnqueue() {
        queue = new StackQueue<>();
        queue.enqueue(1);
        queue.enqueue(2);
        assertEquals(2, queue.size());
    }

    @Test
    void testDequeue() throws EmptyQueueException {
        queue = new StackQueue<>();
        queue.enqueue(1);
        queue.enqueue(2);
        assertEquals(1, queue.dequeue());
        assertEquals(1, queue.size());
    }

    @Test
    void testFirstThrows() {
        queue = new StackQueue<>();
        queue.enqueue(1);
        queue.enqueue(2);
        assertThrows(UnsupportedOperationException.class, () -> queue.first());
    }

    @Test
    void testSize() {
        final int size = 20;
        queue = new StackQueue<>();
        for (int i = 0; i < size; i++) {
            queue.enqueue(i);
        }
        assertEquals(size, queue.size());
    }

    @Test
    void testEmptyQueueException() {
        queue = new StackQueue<>();
        assertThrows(EmptyQueueException.class, () -> queue.dequeue());
    }
}
