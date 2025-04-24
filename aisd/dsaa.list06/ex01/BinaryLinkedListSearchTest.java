package dsaa.list06.ex01;


import dsaa.lab07.TwoWayCycledOrderedListWithSentinel;
import dsaa.util.IList;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static dsaa.util.Common.listToString;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class BinaryLinkedListSearchTest {
    BinaryLinkedListSearch<Integer> searcher = new BinaryLinkedListSearch<>();
    IList<Integer> list;

    @BeforeEach
    public void before() {
        // noinspection unchecked
        list = (IList<Integer>) new TwoWayCycledOrderedListWithSentinel<Integer>();
    }

    @Test
    void testBinaryLinkedListSearch() {
        list.add(4);
        list.add(9);
        list.add(21);
        list.add(5);
        list.add(7);
        list.add(8);
        list.add(6);
        list.add(4);
        list.add(9);
        list.add(21);
        list.add(99);
        list.add(30);
        System.out.println(listToString(list));
        assertEquals(5, searcher.binaryLinkedListSearch(list, Integer::compareTo, 7));
    }
}
