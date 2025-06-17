package dsaa.lab12;

import java.util.LinkedList;

public class Automaton implements IStringMatcher {

    @Override
    public LinkedList<Integer> validShifts(String pattern, String text) {
        // TODO: Implement automaton
        final int patternLength = text.length();
        final int textLength = pattern.length();
        final int maxShift = patternLength - textLength + 1;
        LinkedList<Integer> shifts = new LinkedList<>();
        for (int i = 0; i < maxShift; i++) {
            int j = 0;
            while (j < textLength) {
                if (text.charAt(i + j) == pattern.charAt(j)) {
                    j++;
                } else {
                    break;
                }
            }
            if (j == textLength) {
                shifts.add(i);
            }
        }
        return shifts;
    }

}
