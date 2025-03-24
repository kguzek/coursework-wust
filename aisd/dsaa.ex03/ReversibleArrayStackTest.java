package dsaa.ex03;

import dsaa.util.EmptyStackException;
import dsaa.util.FullStackException;
import dsaa.util.IStack;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ReversibleArrayStackTest {

    private IStack<Integer> stack;
    private static final int CAPACITY = 5;

    @BeforeEach
    void setUp() {
        stack = new ReversibleArrayStack<>(CAPACITY);
    }

    @Test
    void testIsEmptyInitially() {
        assertTrue(stack.isEmpty(), "Stack should be empty initially");
        assertEquals(0, stack.size(), "Initial size should be 0");
    }

    @Test
    void testPushAndTop() throws FullStackException, EmptyStackException {
        stack.push(10);
        assertFalse(stack.isEmpty(), "Stack should not be empty after push");
        assertEquals(10, stack.top(), "Top should return last pushed element");
        assertEquals(1, stack.size(), "Size should be 1 after one push");
    }

    @Test
    void testPushPop() throws FullStackException, EmptyStackException {
        stack.push(20);
        int val = stack.pop();
        assertEquals(20, val, "Popped value should match pushed value");
        assertTrue(stack.isEmpty(), "Stack should be empty after pop");
    }

    @Test
    void testPopEmptyThrowsException() {
        assertThrows(EmptyStackException.class, () -> stack.pop(), "Pop on empty stack should throw");
    }

    @Test
    void testTopEmptyThrowsException() {
        assertThrows(EmptyStackException.class, () -> stack.top(), "Top on empty stack should throw");
    }

    @Test
    void testIsFull() throws FullStackException {
        for (int i = 0; i < CAPACITY; i++) {
            stack.push(i);
        }
        assertTrue(stack.isFull(), "Stack should be full after pushing CAPACITY elements");
        assertThrows(FullStackException.class, () -> stack.push(999), "Pushing to full stack should throw");
    }

    @Test
    void testReverseSingleElement() throws FullStackException, EmptyStackException {
        stack.push(1);
        ((ReversibleArrayStack<Integer>) stack).reverse();
        assertEquals(1, stack.pop(), "Reversing single element stack should not affect order");
    }

    @Test
    void testReverseMultipleElements() throws FullStackException, EmptyStackException {
        stack.push(1);
        stack.push(2);
        stack.push(3); // Stack: [1, 2, 3] => Top is 3

        ((ReversibleArrayStack<Integer>) stack).reverse();
        // Stack should now be [3, 2, 1] => Top is 1

        assertEquals(1, stack.pop(), "First pop after reverse should be 1");
        assertEquals(2, stack.pop(), "Second pop after reverse should be 2");
        assertEquals(3, stack.pop(), "Third pop after reverse should be 3");
        assertTrue(stack.isEmpty(), "Stack should be empty after popping all elements");
    }

    @Test
    void testReverseEmptyStack() {
        ((ReversibleArrayStack<Integer>) stack).reverse();
        assertTrue(stack.isEmpty(), "Reversing empty stack should still be empty");
    }
}