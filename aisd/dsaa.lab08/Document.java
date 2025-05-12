package dsaa.lab08;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@SuppressWarnings("DuplicatedCode")
public class Document implements IWithName {
    private static final Pattern LINK_ID_PATTERN = Pattern.compile("^[a-zA-Z][a-zA-Z0-9_]*$");
    private static final Pattern LINK_PATTERN = Pattern.compile("^([a-zA-Z][a-zA-Z0-9_]*)(?:\\(([0-9]+)\\))?$");
    private static final String LINK_PREFIX = "link=";
    public String name;
    public BST<Link> link;

    public Document(String name) {
        this.name = name.toLowerCase();
        link = new BST<>();
    }

    public Document(String name, Scanner scan) {
        this.name = name.toLowerCase();
        link = new BST<>();
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
        String retStr = "Document: " + name + "\n";
        retStr += link.toStringInOrder();
        return retStr;
    }

    public String toStringPreOrder() {
        String retStr = "Document: " + name + "\n";
        retStr += link.toStringPreOrder();
        return retStr;
    }

    public String toStringPostOrder() {
        String retStr = "Document: " + name + "\n";
        retStr += link.toStringPostOrder();
        return retStr;
    }

    @Override
    public int hashCode() {
        return 0;
    }

    @Override
    public String getName() {
        return name;
    }
}
