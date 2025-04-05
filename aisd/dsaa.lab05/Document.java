package dsaa.lab05;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@SuppressWarnings({"DuplicatedCode", "JavaExistingMethodCanBeUsed"})
public class Document {
    public String name;
    public TwoWayCycledOrderedListWithSentinel<Link> link;
    private static final String LINK_PREFIX = "link=";
    public static final Pattern LINK_ID_PATTERN = Pattern.compile("^[a-zA-Z][a-zA-Z0-9_]*$");
    public static final Pattern LINK_PATTERN = Pattern.compile("^([a-zA-Z][a-zA-Z0-9_]*)(?:\\(([0-9]+)\\))?$");

    public Document(String name, Scanner scan) {
        this.name = name.toLowerCase();
        link = new TwoWayCycledOrderedListWithSentinel<>();
        load(scan);
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
            int current = arr[i];
            int newIndex;
            for (newIndex = i; newIndex < arr.length - 1; newIndex++) {
                if (current < arr[newIndex + 1]) {
                    break;
                }
            }
            if (newIndex != i) {
                // przesuwam połowę posortowanej części w lewo o jedno miejsce
                System.arraycopy(arr, i + 1, arr, i, newIndex - i);
                arr[newIndex] = current;
            }
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
                System.arraycopy(arr, maxIndex + 1, arr, maxIndex, i - maxIndex);
                arr[i] = maxValue;
            }
            showArray(arr);
        }
    }
}
