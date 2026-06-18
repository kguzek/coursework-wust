package dsaa.lab07;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@SuppressWarnings("DuplicatedCode")
public class Document implements IWithName {
    private static final Pattern LINK_ID_PATTERN = Pattern.compile("^[a-zA-Z][a-zA-Z0-9_]*$");
    private static final Pattern LINK_PATTERN = Pattern.compile("^([a-zA-Z][a-zA-Z0-9_]*)(?:\\(([0-9]+)\\))?$");
    private static final String LINK_PREFIX = "link=";
    private final static int[] PRIME_CYCLE = new int[]{7, 11, 13, 17, 19};
    private final static int MOD_VALUE = 100000000;
    public String name;
    public TwoWayCycledOrderedListWithSentinel<Link> link;

    public Document(String name) {
        this.name = name.toLowerCase();
        link = new TwoWayCycledOrderedListWithSentinel<>();
    }

    public Document(String name, Scanner scan) {
        this(name);
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

    public void load(Scanner scan) {
        String line = "";
        while (scan.hasNext() && !line.equals("eod")) {
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

    @Override
    public String getName() {
        return name;
    }

    public boolean equals(Document other) {
        return name.equals(other.name);
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof Document) {
            return equals((Document) other);
        }
        return false;
    }

    @Override
    public int hashCode() {
        if (name.isEmpty()) {
            return 0;
        }
        int sum = Character.hashCode(name.charAt(0));
        for (int i = 1; i < name.length(); i++) {
            char c = name.charAt(i);
            int multiplier = PRIME_CYCLE[(i - 1) % PRIME_CYCLE.length];
            sum = (sum * multiplier + Character.hashCode(c)) % MOD_VALUE;
        }
        return sum;
    }
}
