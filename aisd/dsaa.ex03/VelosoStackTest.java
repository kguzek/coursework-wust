package dsaa.ex03;

import dsaa.util.EmptyStackException;
import dsaa.util.FullStackException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class VelosoStackTest {
    private VelosoStack<Integer> stack;

    @BeforeEach
    void setUp() {
        stack = new VelosoStack<>(3);
    }

    @Test
    void testIsEmptyInitially() {
        assertTrue(stack.isEmpty());
        assertFalse(stack.isFull());
        assertEquals(0, stack.size());
    }

    @Test
    void testPushAndPop() throws FullStackException, EmptyStackException {
        stack.push(10);
        assertFalse(stack.isEmpty());
        assertEquals(1, stack.size());
        assertEquals(10, stack.pop());
        assertTrue(stack.isEmpty());
    }

    @Test
    void testPushBeyondCapacityThrows() throws FullStackException {
        stack.push(1);
        stack.push(2);
        stack.push(3);
        assertTrue(stack.isFull());
        assertThrows(FullStackException.class, () -> stack.push(4));
    }

    @Test
    void testPopFromEmptyThrows() {
        assertThrows(EmptyStackException.class, () -> stack.pop());
    }

    @Test
    void testTopReturnsCorrectElement() throws FullStackException, EmptyStackException {
        stack.push(5);
        stack.push(8);
        assertEquals(null, stack.top());
        assertEquals(2, stack.size()); // Ensure top doesn’t remove
    }

    @Test
    void testPeekEqualsTop() throws FullStackException {
        stack.push(42);
        assertEquals(42, stack.peek()); // Assuming peek works like top()
        assertEquals(1, stack.size());
    }

    @Test
    void testTopAndDownNavigateStack() throws FullStackException, EmptyStackException {
        // Assuming top() moves up pointer, down() moves down, and peek() reads at pointer
        stack.push(1);
        stack.push(2);
        stack.push(3);

        stack.down(); // Move to 2
        assertEquals(2, stack.peek());

        stack.down(); // Move to 1
        assertEquals(1, stack.peek());

        stack.top(); // Move to 3 (top of stack)
        assertEquals(3, stack.peek());
    }

    @Test
    void testDownAtBottomThrows() throws FullStackException {
        stack.push(7);
        assertThrows(IndexOutOfBoundsException.class, () -> stack.down()); // Already at bottom
        assertEquals(7, stack.peek()); // Still at 7
    }

    @Test
    void testTopAtTopRemainsAtTop() throws FullStackException, EmptyStackException {
        stack.push(9);
        stack.top(); // Already at top
        assertEquals(9, stack.peek());
    }
}