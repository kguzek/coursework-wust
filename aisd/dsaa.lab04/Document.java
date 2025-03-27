package dsaa.lab04;

import java.util.Iterator;
import java.util.ListIterator;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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

    @SuppressWarnings("DuplicatedCode")
    public void load(Scanner scan) {
        String line = "";
        while (!line.equals("eod")) {
            line = scan.nextLine();
            String[] words = line.split(" ");
            for (String word : words) {
                if (!word.toLowerCase().startsWith(LINK_PREFIX)) {
                    continue;
                }
                String link = word.substring(LINK_PREFIX.length());
                Link createdLink = createLink(link);
                if (createdLink == null) {
                    continue;
                }
                this.link.add(createdLink);
//                System.out.println(link.toLowerCase());
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
        return idString == null ? new Link(ref) : new Link(ref, Integer.parseInt(idString));
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder("Document: ").append(name);
        Iterator<Link> iter = link.iterator();
        while (iter.hasNext()) {
            StringBuilder subResult = new StringBuilder("\n");
            for (int i = 0; i < 10; i++) {
                Link link = iter.next();
                subResult.append(link);
                if (!iter.hasNext()) {
                    break;
                }
                subResult.append(" ");
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
            for (int i = 0; i < 10; i++) {
                Link link = iter.previous();
                subResult.append(link);
                if (!iter.hasPrevious()) {
                    break;
                }
                subResult.append(" ");
            }
            result.append(subResult);
        }
        return result.toString();
    }
}

