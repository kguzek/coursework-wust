package dsaa.lab12;

import java.util.LinkedList;

public class KMP implements IStringMatcher {

    @Override
    public LinkedList<Integer> validShifts(String pattern, String text) {
        // TODO: Implement KMP
        return new Automaton().validShifts(pattern, text);
    }

}
