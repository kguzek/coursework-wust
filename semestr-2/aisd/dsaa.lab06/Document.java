package dsaa.lab06;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.Scanner;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@SuppressWarnings({"DuplicatedCode", "JavaExistingMethodCanBeUsed"})
public class Document {
    private static final Pattern LINK_ID_PATTERN = Pattern.compile("^[a-zA-Z][a-zA-Z0-9_]*$");
    private static final Pattern LINK_PATTERN = Pattern.compile("^([a-zA-Z][a-zA-Z0-9_]*)(?:\\(([0-9]+)\\))?$");
    private static final String LINK_PREFIX = "link=";
    private static final int MAX_RADIX_VALUE = 999;
    public String name;
    public TwoWayCycledOrderedListWithSentinel<Link> link;

    public Document(String name, Scanner scan) {
        this.name = name.toLowerCase();
        link = new TwoWayCycledOrderedListWithSentinel<>();
        load(scan);
    }

    public static boolean isCorrectId(String id) {
        return LINK_ID_PATTERN.matcher(id).matches();
    }

    // accepts only small letters, capital letters, digits and '_' (except the first character)
    static Link createLink(String link) {
        Matcher matcher = LINK_PATTERN.matcher(link);
        if (!matcher.matches()) {
            return null;
        }
        String ref = matcher.group(1);
        String idString = matcher.group(2);
        int weight = idString == null ? 1 : Integer.parseInt(idString);
        return weight == 0 ? null : new Link(ref, weight);
    }

    public static void showArray(int[] arr) {
        if (arr.length == 0) {
            System.out.println();
            return;
        }
        StringBuilder bob = new StringBuilder(arr.length * 2 - 1).append(arr[0]);
        for (int i = 1; i < arr.length; i++) {
            bob.append(" ").append(arr[i]);
        }
        System.out.println(bob);
    }

    public void load(Scanner scan) {
        String line = "";
        while (!line.equals("eod")) {
            line = scan.nextLine();
            String[] words = line.toLowerCase().split(" ");
            for (String word : words) {
                if (!word.startsWith(LINK_PREFIX)) {
                    continue;
                }
                String link = word.substring(LINK_PREFIX.length());
                Link createdLink = createLink(link);
                if (createdLink == null) {
                    continue;
                }
                this.link.add(createdLink);
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder("Document: ").append(name);
        Iterator<Link> iter = link.iterator();
        while (iter.hasNext()) {
            StringBuilder subResult = new StringBuilder("\n");
            for (int i = 0; i < 9; i++) {
                subResult.append(iter.next());
                if (!iter.hasNext()) {
                    break;
                }
                subResult.append(" ");
            }
            if (iter.hasNext()) {
                subResult.append(iter.next());
            }
            result.append(subResult);
        }
        return result.toString();
    }

    public String toStringReverse() {
        StringBuilder result = new StringBuilder("Document: ").append(name);
        ListIterator<Link> iter = link.listIterator();
        while (iter.hasNext()) iter.next();
        while (iter.hasPrevious()) {
            StringBuilder subResult = new StringBuilder("\n");
            for (int i = 0; i < 9; i++) {
                subResult.append(iter.previous());
                if (!iter.hasPrevious()) {
                    break;
                }
                subResult.append(" ");
            }
            if (iter.hasPrevious()) {
                subResult.append(iter.previous());
            }
            result.append(subResult);
        }
        return result.toString();
    }

    public int[] getWeights() {
        int[] weights = new int[link.size()];
        Iterator<Link> iter = link.iterator();
        for (int i = 0; iter.hasNext(); i++) {
            weights[i] = iter.next().weight;
        }
        return weights;
    }

    void bubbleSort(int[] arr) {
        showArray(arr);
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = arr.length - 1; j > i; j--) {
                if (arr[j] < arr[j - 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j - 1];
                    arr[j - 1] = temp;
                }
            }
            showArray(arr);
        }
    }

    public void insertSort(int[] arr) {
        showArray(arr);
        for (int i = arr.length - 2; i >= 0; i--) {
            int value = arr[i];
            int j = i;
            while (j < arr.length - 1 && value > arr[j + 1]) {
                arr[j] = arr[j + 1];
                j++;
            }
            arr[j] = value;
            showArray(arr);
        }
    }

    public void selectSort(int[] arr) {
        showArray(arr);
        for (int i = arr.length - 1; i > 0; i--) {
            int maxIndex = 0;
            for (int j = 1; j <= i; j++) {
                if (arr[j] > arr[maxIndex]) {
                    maxIndex = j;
                }
            }
            if (maxIndex != i) {
                int maxValue = arr[maxIndex];
                arr[maxIndex] = arr[i];
                arr[i] = maxValue;
            }
            showArray(arr);
        }
    }


    public void iterativeMergeSort(int[] arr) {
        showArray(arr);
        int subLength = 1;
        int leftIndex;
        int rightIndex;
        int currentIndex;
        int[] tempArray = new int[arr.length];
        while (subLength < arr.length) {
            final int splitLength = subLength * 2;
            for (int blockIndex = 0; blockIndex * splitLength < arr.length; blockIndex++) {
                final int blockStart = blockIndex * splitLength;
                final int endIndex = Math.min(arr.length, blockStart + splitLength);
                leftIndex = blockStart;
                rightIndex = leftIndex + subLength;
                for (currentIndex = blockStart; currentIndex < endIndex; currentIndex++) {
                    int relativeIndex = currentIndex - blockStart;
                    boolean leftValid = leftIndex < blockStart + subLength;
                    boolean rightValid = rightIndex < endIndex;
                    if (leftValid && (!rightValid || arr[leftIndex] < arr[rightIndex])) {
                        tempArray[relativeIndex] = arr[leftIndex++];
                    } else if (rightValid) {
                        tempArray[relativeIndex] = arr[rightIndex++];
                    }
                }
                System.arraycopy(tempArray, 0, arr, blockStart, endIndex - blockStart);
            }
            subLength = splitLength;
            showArray(arr);
        }
    }

    @SuppressWarnings("SameParameterValue")
    private void countSort(int[] arr, int d, Function<Integer, Integer> mapper) {
        int[] occurrences = new int[d];
        for (int j : arr) {
            occurrences[mapper.apply(j)]++;
        }
        int[] startIndexes = new int[d];
        for (int i = 1; i < occurrences.length; i++) {
            int previousIndex = i - 1;
            startIndexes[i] = startIndexes[previousIndex] + occurrences[previousIndex];
        }
        int[] result = new int[arr.length];
        for (int j : arr) {
            int mappedResult = mapper.apply(j);
            result[startIndexes[mappedResult]++] = j;
        }
        System.arraycopy(result, 0, arr, 0, arr.length);
        showArray(arr);
    }

    public void radixSort(int[] arr) {
        showArray(arr);
        int maxValue = MAX_RADIX_VALUE;
        for (int j : arr) {
            if (j > maxValue) {
                maxValue = j;
            }
        }
        for (int radix = 1; radix <= maxValue; radix *= 10) {
            final int finalRadix = radix;
            countSort(arr, 10, (Integer a) -> (a / finalRadix % 10));
        }
//        showArray(arr);
    }
}
