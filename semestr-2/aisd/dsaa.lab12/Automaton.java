package dsaa.lab12;

import java.util.LinkedList;

public class Automaton implements IStringMatcher {

    private static final int DEFAULT_ALPHABET_SIZE = 256;  // number of unique ASCII characters by default

    private int nextState(String pattern, int patternIndex, int character) {
        final int patternLength = pattern.length();
        if (patternIndex < patternLength && character == pattern.charAt(patternIndex)) {
            return patternIndex + 1;
        }
        int i;
        for (int next = patternIndex; next > 0; next--) {
            if (pattern.charAt(next - 1) == character) {
                for (i = 0; i < next - 1; i++) {
                    if (pattern.charAt(i) != pattern.charAt(patternIndex - next + i + 1)) {
                        break;
                    }
                }
                if (i == next - 1) {
                    return next;
                }
            }
        }
        return 0;
    }

    private int[][] buildAutomaton(String pattern, @SuppressWarnings("SameParameterValue") final int alphabetSize) {
        int patternLength = pattern.length();
        int[][] dfa = new int[patternLength + 1][alphabetSize];
        for (int i = 0; i <= patternLength; i++) {
            for (int j = 0; j < alphabetSize; j++) {
                dfa[i][j] = nextState(pattern, i, j);
            }
        }
        return dfa;
    }

    private int[][] buildAutomaton(String pattern) {
        return buildAutomaton(pattern, DEFAULT_ALPHABET_SIZE);
    }

    @Override
    public LinkedList<Integer> validShifts(String pattern, String text) {
        final int patternLength = pattern.length();
        final int textLength = text.length();
        LinkedList<Integer> shifts = new LinkedList<>();

        if (patternLength == 0 || textLength < patternLength) {
            return shifts;
        }

        int[][] dfa = buildAutomaton(pattern);
        int state = 0;
        for (int i = 0; i < textLength; i++) {
            state = dfa[state][text.charAt(i)]; // implicit cast from char to ASCII index
            if (state == patternLength) {
                shifts.add(i - patternLength + 1); // match found
            }
        }
        return shifts;
    }

}
