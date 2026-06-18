package dsaa.list03.ex05;

import dsaa.util.EmptyQueueException;

public class Josephus {
    /**
     * Performs a computation of the Josephus problem. Given a number of elements n and a number k, this method
     * returns the last element present after every kth element is removed until only one remains.
     */
    public static int josephus(int n, int k) {
        ListQueue<Integer> queue = new ListQueue<>();
        for (int i = 0; i < n; i++) {
            queue.enqueue(i);
        }
        try {
            while (queue.size() > 1) {
                for (int i = 1; i < k; i++) {
                    queue.enqueue(queue.dequeue());
                }
                queue.dequeue();
            }
            return queue.dequeue();
        } catch (EmptyQueueException e) {
            assert false : "Could not dequeue the queue";
        }
        return -1;
    }
}
