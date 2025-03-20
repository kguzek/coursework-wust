package dsaa.lab03;

import java.util.Scanner;

public class Document {
    public String name;
    public TwoWayUnorderedListWithHeadAndTail<Link> link;
    private static final String LINK_PREFIX = "link=";

    public Document(String name, Scanner scan) {
        this.name = name;
        link = new TwoWayUnorderedListWithHeadAndTail<>();
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
                if (!correctLink(link)) {
                    continue;
                }
                this.link.add(new Link(link));
//                System.out.println(link.toLowerCase());
            }
        }
    }

    // accepts only small letters, capital letters, digits and '_' (except the first character)
    @SuppressWarnings({"JavaExistingMethodCanBeUsed", "DuplicatedCode"})
    public static boolean correctLink(String link) {
        if (link.isEmpty()) {
            return false;
        }
        if (!Character.isLetter(link.charAt(0))) {
            return false;
        }
        for (int i = 1; i < link.length(); i++) {
            char c = link.charAt(i);
            if (!Character.isLetter(c) && !Character.isDigit(c) && c != '_') {
                return false;
            }
        }
        return true;
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder("Document: ").append(name);
        for (Link link : link) {
            result.append("\n").append(link.ref);
        }
        return result.toString();
    }

    public String toStringReverse() {
        String retStr = "Document: " + name;
        return retStr + link.toStringReverse();
    }

}
