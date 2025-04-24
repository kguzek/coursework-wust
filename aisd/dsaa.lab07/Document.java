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
    public String name;
    public TwoWayCycledOrderedListWithSentinel<Link> link;

    public Document(String name) {
        // TODO
        this(name, new Scanner(System.in));
    }

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

    @Override
    public String getName() {
        // TODO
        return null;
    }


}

