package dsaa.lab12;

import java.util.LinkedList;

public class Automaton implements IStringMatcher {

    @Override
    public LinkedList<Integer> validShifts(String pattern, String text) {
        // TODO: Implement automaton
        final int patternLength = pattern.length();
        LinkedList<Integer> shifts = new LinkedList<>();
        if (patternLength == 0) {
            return shifts;
        }
        final int textLength = text.length();
        final int maxShift = textLength - patternLength + 1;
        for (int i = 0; i < maxShift; i++) {
            int j = 0;
            while (j < patternLength) {
                if (text.charAt(i + j) == pattern.charAt(j)) {
                    j++;
                } else {
                    break;
                }
            }
            if (j == patternLength) {
                shifts.add(i);
            }
        }
        return shifts;
    }
}
