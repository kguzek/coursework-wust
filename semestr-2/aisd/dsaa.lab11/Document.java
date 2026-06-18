package dsaa.lab11;

import java.util.Scanner;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@SuppressWarnings("DuplicatedCode")
public class Document implements IWithName {
    private static final Pattern LINK_ID_PATTERN = Pattern.compile("^[a-zA-Z][a-zA-Z0-9_]*$");
    private static final Pattern LINK_PATTERN = Pattern.compile("^([a-zA-Z][a-zA-Z0-9_]*)(?:\\(([0-9]+)\\))?$");
    private static final String LINK_PREFIX = "link=";
    public String name;
    public SortedMap<String, Link> link;

    public Document(String name) {
        this.name = name.toLowerCase();
        link = new TreeMap<>();
    }

    public Document(String name, Scanner scan) {
        this.name = name.toLowerCase();
        link = new TreeMap<>();
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
                String ref = word.substring(LINK_PREFIX.length());
                Link createdLink = createLink(ref);
                if (createdLink == null) {
                    continue;
                }
                link.put(createdLink.ref, createdLink);
            }
        }
    }

    @Override
    public String toString() {
        String retStr = "Document: " + name + "\n";
        retStr += link.toString();
        return retStr;
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }

    @Override
    public String getName() {
        return name;
    }
}
