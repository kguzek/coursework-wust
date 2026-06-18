package dsaa.lab12;

import java.util.LinkedList;

public class KMP implements IStringMatcher {

    private int[] generatePiArray(String pattern) {
        final int patternLength = pattern.length();
        int[] pi = new int[patternLength];
        int j = 0;
        for (int i = 1; i < patternLength; i++) {
            char current = pattern.charAt(i);
            while (j > 0 && current != pattern.charAt(j)) {
                j = pi[j - 1];
            }
            if (current == pattern.charAt(j)) {
                j++;
            }
            pi[i] = j;
        }
        return pi;
    }

    @Override
    public LinkedList<Integer> validShifts(String pattern, String text) {
        final int[] pi = generatePiArray(pattern);
        final int patternLength = pattern.length();
        final int textLength = text.length();
        final LinkedList<Integer> shifts = new LinkedList<>();
        if (patternLength == 0) {
            return shifts;
        }
        int i = 0;
        int j = 0;
        while (i < textLength) {
            if (pattern.charAt(j) == text.charAt(i)) {
                j++;
                i++;
            } else if (j == 0) {
                i++;
            } else {
                j = pi[j - 1];
            }
            if (j == patternLength) {
                shifts.addLast(i - patternLength);
                j = pi[j - 1];
            }
        }
        return shifts;
    }
}
