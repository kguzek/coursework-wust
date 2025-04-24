package dsaa.list06.ex01;


import dsaa.lab07.IList;
import dsaa.lab07.TwoWayCycledOrderedListWithSentinel;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static dsaa.util.Common.listToString;

public class BinaryLinkedListSearchTest {
    BinaryLinkedListSearch<Integer> searcher = new BinaryLinkedListSearch<>();
    IList<Integer> list;

    @BeforeEach
    public void before() {
        list = new TwoWayCycledOrderedListWithSentinel<>();
    }

    @Test
    void testBinaryLinkedListSearch() {
//        Generate random values in list
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
    }
}
